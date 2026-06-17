"""Assembly-level FASTA validation and descriptive QC; no completeness estimate."""
from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path

from .data_acquisition import records


def fasta_lengths(path: Path) -> tuple[list[int], int, int]:
    opener = gzip.open if path.suffix == ".gz" else open
    lengths, seen, length, gc, ambiguous = [], set(), 0, 0, 0
    with opener(path, "rt", encoding="ascii") as handle:
        for line in handle:
            line = line.strip().upper()
            if not line:
                continue
            if line.startswith(">"):
                identifier = line[1:].split()[0]
                if not identifier or identifier in seen:
                    raise ValueError(f"Missing or duplicate FASTA identifier in {path}")
                seen.add(identifier)
                if len(seen) > 1:
                    lengths.append(length)
                length = 0
            else:
                if not seen or any(c not in "ACGTN" for c in line):
                    raise ValueError(f"Invalid FASTA sequence in {path}")
                length += len(line)
                gc += line.count("G") + line.count("C")
                ambiguous += line.count("N")
    if not seen or not length:
        raise ValueError(f"Empty FASTA in {path}")
    lengths.append(length)
    return lengths, gc, ambiguous


def metrics(path: Path) -> dict[str, object]:
    lengths, gc, ambiguous = fasta_lengths(path)
    total = sum(lengths)
    running = 0
    n50 = 0
    for length in sorted(lengths, reverse=True):
        running += length
        if running >= total / 2:
            n50 = length
            break
    return {"assembly_length_bp": total, "gc_percent": round(100 * gc / total, 3),
            "contig_count": len(lengths), "n50_bp": n50,
            "ambiguous_percent": round(100 * ambiguous / total, 5)}


def run(manifest: Path, raw: Path, result: Path) -> None:
    output = []
    for row in records(manifest):
        accession = row["assembly_accession"]
        path = raw / f"{accession}.fna.gz"
        record: dict[str, object] = {"assembly_accession": accession}
        try:
            if not path.exists():
                raise FileNotFoundError(path)
            record.update(metrics(path))
            record["qc_status"] = ("pass" if 2_500_000 <= record["assembly_length_bp"] <= 3_200_000
                                   and record["contig_count"] <= 20
                                   and record["ambiguous_percent"] <= 1 else "review")
            record["qc_note"] = "" if record["qc_status"] == "pass" else "Outside exploratory size/fragmentation/N screen"
        except (OSError, ValueError) as error:
            record.update({"qc_status": "fail", "qc_note": str(error)})
        output.append(record)
    result.parent.mkdir(parents=True, exist_ok=True)
    columns = ["assembly_accession", "assembly_length_bp", "gc_percent", "contig_count", "n50_bp", "ambiguous_percent", "qc_status", "qc_note"]
    with result.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader(); writer.writerows(output)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/metadata/genome_manifest.csv"))
    p.add_argument("--raw", type=Path, default=Path("data/raw"))
    p.add_argument("--result", type=Path, default=Path("results/genome_qc.csv"))
    a = p.parse_args(); run(a.manifest, a.raw, a.result)

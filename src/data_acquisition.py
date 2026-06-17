"""Download versioned RefSeq assemblies listed in the manifest."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import re
import urllib.request
from pathlib import Path

ACCESSION = re.compile(r"^GCF_\d{9}\.\d+$")


def records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"assembly_accession", "genome_url", "biosample_accession"} <= rows[0].keys():
        raise ValueError("Manifest is empty or missing required columns")
    ids = [r["assembly_accession"] for r in rows]
    if len(ids) != len(set(ids)) or any(not ACCESSION.fullmatch(x) for x in ids):
        raise ValueError("Duplicate or invalid versioned RefSeq accession")
    for row in rows:
        if not row["genome_url"].startswith("https://ftp.ncbi.nlm.nih.gov/genomes/all/"):
            raise ValueError(f"Unexpected genome URL for {row['assembly_accession']}")
    return rows


def download(manifest: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    expected_path = manifest.parent / "download_checksums.tsv"
    expected = {}
    if expected_path.exists():
        with expected_path.open(newline="", encoding="utf-8") as handle:
            expected = {r["assembly_accession"]: r["sha256"] for r in csv.DictReader(handle, delimiter="\t")}
    for row in records(manifest):
        accession = row["assembly_accession"]
        target = output / f"{accession}.fna.gz"
        if target.exists():
            if accession in expected and hashlib.sha256(target.read_bytes()).hexdigest() != expected[accession]:
                raise ValueError(f"Checksum mismatch for existing {target}")
            print(f"existing {accession}")
            continue
        temp = target.with_suffix(".part")
        try:
            urllib.request.urlretrieve(row["genome_url"], temp)
            with gzip.open(temp, "rb") as stream:
                if stream.read(1) != b">":
                    raise ValueError("Download is not FASTA")
                while stream.read(1024 * 1024):
                    pass  # verify gzip CRC
            if accession in expected and hashlib.sha256(temp.read_bytes()).hexdigest() != expected[accession]:
                raise ValueError(f"Checksum mismatch for downloaded {accession}")
            temp.replace(target)
            print(f"downloaded {accession}")
        finally:
            temp.unlink(missing_ok=True)
    with (output / "sha256.tsv").open("w", encoding="utf-8") as handle:
        handle.write("assembly_accession\tsha256\n")
        for row in records(manifest):
            target = output / f"{row['assembly_accession']}.fna.gz"
            if target.exists():
                handle.write(f"{row['assembly_accession']}\t{hashlib.sha256(target.read_bytes()).hexdigest()}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("data/metadata/genome_manifest.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    download(args.manifest, args.output)

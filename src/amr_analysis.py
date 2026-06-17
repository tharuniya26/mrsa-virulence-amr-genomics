"""Run NCBI AMRFinderPlus; retain its full native output and parsed AMR calls."""
from __future__ import annotations

import argparse
import csv
import gzip
import shutil
import subprocess
from datetime import date
from pathlib import Path

from .data_acquisition import records

FIELDS = ["assembly_accession", "gene_symbol", "element_type", "element_subtype", "class", "subclass", "method", "reference_accession", "identity_percent", "coverage_percent", "tool_version", "database_version", "analysis_date"]


def parse_amrfinder(path: Path, accession: str, tool_version: str, db_version: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"Element symbol", "Element type", "Class", "Method", "Accession of closest sequence"}
        if not reader.fieldnames or not required <= set(reader.fieldnames):
            raise ValueError(f"Unexpected AMRFinderPlus columns in {path}")
        return [{"assembly_accession": accession, "gene_symbol": r.get("Element symbol", ""),
                 "element_type": r.get("Element type", ""), "element_subtype": r.get("Element subtype", ""),
                 "class": r.get("Class", ""), "subclass": r.get("Subclass", ""), "method": r.get("Method", ""),
                 "reference_accession": r.get("Accession of closest sequence", ""),
                 "identity_percent": r.get("% Identity to reference sequence", ""),
                 "coverage_percent": r.get("% Coverage of reference sequence", ""),
                 "tool_version": tool_version, "database_version": db_version, "analysis_date": date.today().isoformat()}
                for r in reader if r.get("Element type", "").upper() == "AMR"]


def run(manifest: Path, raw: Path, results: Path) -> None:
    if not shutil.which("amrfinder"):
        raise RuntimeError("amrfinder unavailable. Install NCBI AMRFinderPlus in the documented Conda environment.")
    version = subprocess.run(["amrfinder", "--version"], capture_output=True, text=True, check=True).stdout.strip()
    db_version = subprocess.run(["amrfinder", "--database_version"], capture_output=True, text=True, check=True).stdout.strip()
    results.mkdir(parents=True, exist_ok=True)
    calls = []
    for row in records(manifest):
        acc = row["assembly_accession"]
        source = raw / f"{acc}.fna.gz"
        if not source.exists():
            raise FileNotFoundError(source)
        fasta = results / f"{acc}.fna"
        native = results / f"{acc}.amrfinder.tsv"
        with gzip.open(source, "rb") as src, fasta.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        try:
            with native.open("w", encoding="utf-8") as out:
                subprocess.run(["amrfinder", "--nucleotide", str(fasta), "--organism", "Staphylococcus_aureus", "--plus"], stdout=out, check=True)
            calls.extend(parse_amrfinder(native, acc, version, db_version))
        finally:
            fasta.unlink(missing_ok=True)
    with (results / "amr_gene_calls.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, FIELDS); writer.writeheader(); writer.writerows(calls)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/metadata/genome_manifest.csv"))
    p.add_argument("--raw", type=Path, default=Path("data/raw"))
    p.add_argument("--results", type=Path, default=Path("results"))
    a = p.parse_args(); run(a.manifest, a.raw, a.results)

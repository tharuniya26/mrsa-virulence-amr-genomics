"""Extract explicitly named virulence calls from AMRFinderPlus native TSV."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .data_acquisition import records

TARGETS = {"lukS-PV", "lukF-PV", "hla", "hlb", "hld", "clfA", "clfB", "fnbA", "fnbB"}


def parse_virulence(path: Path, accession: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames or not {"Element symbol", "Element type", "Method"} <= set(reader.fieldnames):
            raise ValueError(f"Unexpected AMRFinderPlus columns in {path}")
        return [{"assembly_accession": accession, "gene_symbol": r["Element symbol"],
                 "method": r["Method"], "reference_accession": r.get("Accession of closest sequence", ""),
                 "identity_percent": r.get("% Identity to reference sequence", ""),
                 "coverage_percent": r.get("% Coverage of reference sequence", ""),
                 "target_panel_member": str(r["Element symbol"] in TARGETS).lower()}
                for r in reader if r.get("Element type", "").upper() == "VIRULENCE"]


def run(manifest: Path, results: Path) -> None:
    calls = []
    for row in records(manifest):
        accession = row["assembly_accession"]
        native = results / f"{accession}.amrfinder.tsv"
        if not native.exists():
            raise FileNotFoundError(f"Run src.amr_analysis first: {native}")
        calls.extend(parse_virulence(native, accession))
    fields = ["assembly_accession", "gene_symbol", "method", "reference_accession", "identity_percent", "coverage_percent", "target_panel_member"]
    with (results / "virulence_gene_calls.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields); writer.writeheader(); writer.writerows(calls)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/metadata/genome_manifest.csv"))
    p.add_argument("--results", type=Path, default=Path("results"))
    a = p.parse_args(); run(a.manifest, a.results)

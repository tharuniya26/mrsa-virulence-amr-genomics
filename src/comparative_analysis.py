"""Join QC and verified positive gene calls without converting unassessed to absent."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def run(manifest: Path, results: Path) -> None:
    meta = pd.read_csv(manifest, keep_default_na=False)
    qc = pd.read_csv(results / "genome_qc.csv", keep_default_na=False)
    if meta.assembly_accession.duplicated().any() or qc.assembly_accession.duplicated().any():
        raise ValueError("Duplicate assembly identifiers")
    merged = meta.merge(qc, on="assembly_accession", validate="one_to_one")
    for kind in ("amr", "virulence"):
        path = results / f"{kind}_gene_calls.csv"
        if path.exists():
            calls = pd.read_csv(path, keep_default_na=False)
            unknown = set(calls.assembly_accession) - set(meta.assembly_accession)
            if unknown:
                raise ValueError(f"Unknown {kind} accessions: {unknown}")
            names = calls.groupby("assembly_accession").gene_symbol.apply(lambda x: ";".join(sorted(set(x))))
            merged[f"{kind}_detected_genes"] = merged.assembly_accession.map(names).fillna("")
            merged[f"{kind}_assessment"] = "completed_positive_calls_only"
        else:
            merged[f"{kind}_detected_genes"] = ""
            merged[f"{kind}_assessment"] = "not_assessed"
    merged.to_csv(results / "comparative_genomics_summary.csv", index=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/metadata/genome_manifest.csv"))
    p.add_argument("--results", type=Path, default=Path("results"))
    a = p.parse_args(); run(a.manifest, a.results)

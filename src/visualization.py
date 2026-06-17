"""Figures from observed assembly QC only."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def qc_figure(qc_file: Path, figures: Path) -> None:
    data = pd.read_csv(qc_file)
    clean = data.loc[data.qc_status == "pass"].copy()
    if clean.empty:
        raise ValueError("No QC-passing genomes available for plotting")
    figures.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5), layout="constrained")
    labels = clean.assembly_accession.str.replace("GCF_", "", regex=False)
    axes[0].bar(labels, clean.assembly_length_bp / 1e6, color="#27678b")
    axes[0].set_ylabel("Assembly length (Mbp)")
    axes[1].bar(labels, clean.contig_count, color="#6b9a77")
    axes[1].set_ylabel("Sequence records")
    for axis in axes:
        axis.tick_params(axis="x", rotation=45)
        axis.set_xlabel("RefSeq assembly accession")
    fig.suptitle("Public S. aureus reference assembly QC")
    for suffix in ("png", "svg"):
        fig.savefig(figures / f"genome_qc.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--qc", type=Path, default=Path("results/genome_qc.csv"))
    p.add_argument("--figures", type=Path, default=Path("figures"))
    a = p.parse_args(); qc_figure(a.qc, a.figures)

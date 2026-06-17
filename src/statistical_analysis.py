"""Descriptive summaries and Wilson intervals for fully assessed binary outcomes."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def wilson(successes: int, total: int, z: float = 1.95996398454) -> tuple[float, float]:
    if total <= 0 or not 0 <= successes <= total:
        raise ValueError("Require 0 <= successes <= total and total > 0")
    p = successes / total
    denom = 1 + z*z/total
    center = (p + z*z/(2*total)) / denom
    radius = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / denom
    return center-radius, center+radius


def run(qc_file: Path, result: Path) -> None:
    with qc_file.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    passed = sum(r["qc_status"] == "pass" for r in rows)
    result.write_text(f"Genomes selected: {len(rows)}\nGenomes passing exploratory assembly QC: {passed}\n"
                      "No marker prevalence calculated because a validated complete marker assessment is unavailable.\n", encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--qc", type=Path, default=Path("results/genome_qc.csv"))
    p.add_argument("--result", type=Path, default=Path("results/descriptive_summary.txt"))
    a = p.parse_args(); run(a.qc, a.result)

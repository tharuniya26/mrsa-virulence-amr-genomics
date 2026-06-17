import csv
import gzip
from pathlib import Path

import pytest

from src.data_acquisition import records
from src.genome_qc import metrics
from src.amr_analysis import parse_amrfinder
from src.virulence_analysis import parse_virulence
from src.statistical_analysis import wilson
from src.visualization import qc_figure


def test_manifest_duplicate_rejected(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text("assembly_accession,biosample_accession,genome_url\nGCF_000000001.1,SAMN1,https://ftp.ncbi.nlm.nih.gov/genomes/all/x\nGCF_000000001.1,SAMN1,https://ftp.ncbi.nlm.nih.gov/genomes/all/x\n")
    with pytest.raises(ValueError, match="Duplicate"):
        records(p)


def test_qc_and_invalid_fasta(tmp_path):
    p = tmp_path / "good.fna.gz"
    with gzip.open(p, "wt") as handle: handle.write(">chr\nACGNN\n>plasmid\nGGCC\n")
    assert metrics(p)["n50_bp"] == 5
    assert metrics(p)["ambiguous_percent"] == pytest.approx(22.22222, abs=.00001)
    with gzip.open(p, "wt") as handle: handle.write(">same\nACGT\n>same\nACGT\n")
    with pytest.raises(ValueError, match="duplicate"):
        metrics(p)


def test_amr_and_virulence_parsers(tmp_path):
    p = tmp_path / "native.tsv"
    p.write_text("Element symbol\tElement type\tClass\tMethod\tAccession of closest sequence\n"
                 "mecA\tAMR\tBETA-LACTAM\tEXACTP\tABC1\n"
                 "lukS-PV\tVIRULENCE\t\tBLASTP\tABC2\n")
    assert parse_amrfinder(p, "GCF_000000001.1", "tool", "db")[0]["gene_symbol"] == "mecA"
    assert parse_virulence(p, "GCF_000000001.1")[0]["target_panel_member"] == "true"


def test_wilson_and_plot(tmp_path):
    low, high = wilson(2, 4)
    assert low < .5 < high
    with pytest.raises(ValueError): wilson(0, 0)
    qc = tmp_path / "qc.csv"
    with qc.open("w", newline="") as handle:
        w = csv.DictWriter(handle, ["assembly_accession", "assembly_length_bp", "contig_count", "qc_status"])
        w.writeheader(); w.writerow({"assembly_accession": "GCF_000000001.1", "assembly_length_bp": 2800000, "contig_count": 1, "qc_status": "pass"})
    qc_figure(qc, tmp_path)
    assert (tmp_path / "genome_qc.svg").exists()

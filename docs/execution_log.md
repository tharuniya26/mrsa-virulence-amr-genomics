# Validation execution log — 6 November 2026

This log records the local validation performed from the repository root. It is a status record, not evidence that unavailable genomic analyses succeeded.

## Environment

- Host: Windows, PowerShell
- Python: 3.14.2
- pandas: 3.0.6
- Matplotlib: 3.11.2
- pytest: 9.1.1
- AMRFinderPlus: unavailable (`amrfinder` not found)
- MLST: unavailable (`mlst` not found)
- SCCmec typing software/database: unavailable
- Conda/Mamba/Docker: unavailable
- WSL: executable present, but no installed Linux distribution was available

## Commands and outcomes

| Command or check | Outcome |
|---|---|
| `python -m src.data_acquisition` | Passed; all four files reported `existing` and matched tracked SHA-256 values |
| `python -m src.genome_qc` | Passed; regenerated `results/genome_qc.csv` with no result diff |
| `python -m src.visualization` | Passed after selecting the headless `Agg` backend |
| `python -m src.diagrams` | Passed; conceptual figures regenerated |
| `python -m src.comparative_analysis` | Passed; marker assessments remain `not_assessed` |
| `python -m src.statistical_analysis` | Passed; no marker prevalence was calculated |
| `python -m pytest -q -p no:cacheprovider` | Passed: 4/4 tests |
| Execute `notebooks/01` through `notebooks/06` in memory with `nbclient` | Passed: 6/6 notebooks |
| Repeat all PNG/SVG figure builds and compare SHA-256 values | Passed; each pair of repeated builds was byte-identical |
| Visual inspection of all three PNG figures | Passed; labels and content match their documented result/conceptual status |
| `python -m src.amr_analysis` | Stopped as designed: AMRFinderPlus executable unavailable |
| `python -m src.virulence_analysis` | Stopped as designed: native AMRFinderPlus TSVs do not exist |
| `python reports/build_latex.py` | Passed; `pdflatex`/BibTeX completed and rebuilt the 9-page PDF |
| Render and inspect all PDF pages | Passed; no clipping, overflow, missing table/figure, or missing reference was observed |

The first plotting attempt exposed a Tk backend failure on this minimal Python installation. The plotting modules now select `Agg`, and both the test suite and direct figure commands pass. QC validation also now rejects an empty intermediate FASTA record; a regression assertion was added.

## Scientific result boundary

Executed outputs support only accession provenance, compressed-file integrity, elementary assembly metrics, the predefined exploratory QC decision, and integration of QC with the manifest. No AMR determinant, virulence-associated gene, sequence type, SCCmec type, phenotype, phylogeny or population frequency was generated or inferred.

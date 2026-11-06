# Project audit — revalidated 6 November 2026

| Review item | Status | Evidence / next action |
|---|---|---|
| Original MRSA source separated from unrelated material | PASSED | `source_review.md`; original DOCX remains outside repo unchanged. |
| Public source-figure rights | NOT VERIFIED | `source_image_inventory.md`; no embedded source figure republished. |
| NCBI accession and BioSample provenance | PASSED | Four versioned RefSeq URLs and BioSample IDs in the manifest; linked NCBI records in `dataset_selection.md`. |
| Download integrity and raw FASTA validity | PASSED | Four gzip streams parsed; all four compressed-file SHA-256 values match the tracked table; duplicate, invalid and empty-record FASTA cases are rejected. |
| Assembly QC | PASSED | Four actual assemblies in `results/genome_qc.csv`; all pass the predefined exploratory size/fragmentation/N screen. |
| Completeness and contamination assessment | NOT VERIFIED | Run a validated bacterial completeness/contamination tool before stronger assembly-quality claims. |
| AMR gene calls and gene matrix | NOT PERFORMED | `python -m src.amr_analysis` was attempted and stopped explicitly because the AMRFinderPlus executable/database are unavailable. No native TSV or gene matrix exists. |
| Virulence calls and PVL status | NOT PERFORMED | Native AMRFinderPlus output does not exist; target-reference coverage, partial hits and ambiguous hits therefore cannot be reviewed. |
| MLST and SCCmec typing | NOT PERFORMED | Dedicated typing software/databases are unavailable; no values were inferred from strain names or literature. |
| Phenotypic susceptibility comparison | NOT APPLICABLE | No authenticated AST metadata for the selected assemblies. |
| Epidemiological group comparison | NOT APPLICABLE | Acquisition setting not verified consistently across these specimens. |
| Statistical inference and population prevalence | NOT APPLICABLE | Four selected historic references are not an independent representative sample. |
| QC figure and conceptual figures | PASSED | PNG/SVG produced from observed QC or explicitly labelled biological schema. |
| Six clean notebooks | PASSED | All 6/6 notebooks executed successfully in memory from the repository root; tracked notebooks remain clean and contain no stored outputs. |
| Standalone report | PASSED | Scientific statements and tabulated QC values were checked against executed outputs; LaTeX source, BibTeX and PDF distinguish completed QC from unavailable analyses. |
| Automated code tests | PASSED | 4/4 tests pass and cover manifest validation, FASTA QC (including empty records), caller parsing, Wilson calculation and headless plot creation. |
| Figure reproducibility | PASSED | All three PNG/SVG figure pairs regenerated; repeated runs produced identical SHA-256 values and visual inspection found no clipping or label errors. |
| Scoped repository release | READY WITH LIMITATIONS | Code, QC outputs and documentation are suitable for release only with the explicit statement that molecular screening and typing were not performed. |

**Specific completion path:** run AMRFinderPlus with a recorded database version in a supported environment, validate reference coverage for target genes, inspect native output, perform typing with dedicated methods if desired, and seek authentic phenotype and epidemiological metadata before making those comparisons. See [`execution_log.md`](execution_log.md) for commands and environment details. Rebuild the report and audit after any new molecular results are verified.

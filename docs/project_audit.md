# Project audit — 17 October 2026

| Review item | Status | Evidence / next action |
|---|---|---|
| Original MRSA source separated from unrelated material | PASSED | `source_review.md`; original DOCX remains outside repo unchanged. |
| Public source-figure rights | NOT VERIFIED | `source_image_inventory.md`; no embedded source figure republished. |
| NCBI accession and BioSample provenance | PASSED | Four versioned RefSeq URLs and BioSample IDs in the manifest; linked NCBI records in `dataset_selection.md`. |
| Download integrity and raw FASTA validity | PASSED | Four gzip streams parsed; local SHA-256 table generated; duplicate and invalid identifiers rejected by QC. |
| Assembly QC | PASSED | Four actual assemblies in `results/genome_qc.csv`; all pass the predefined exploratory size/fragmentation/N screen. |
| Completeness and contamination assessment | NOT VERIFIED | Run a validated bacterial completeness/contamination tool before stronger assembly-quality claims. |
| AMR gene calls and gene matrix | NOT VERIFIED | AMRFinderPlus executable/database unavailable on this Windows host. Run `src.amr_analysis` in Linux Conda, capture versions and review native TSVs. |
| Virulence calls and PVL status | NOT VERIFIED | Requires AMRFinderPlus execution plus target-reference coverage audit; review partial and ambiguous hits. |
| MLST and SCCmec typing | NOT VERIFIED | Dedicated typing tools and cassette-level review required; no values fabricated. |
| Phenotypic susceptibility comparison | NOT APPLICABLE | No authenticated AST metadata for the selected assemblies. |
| Epidemiological group comparison | NOT APPLICABLE | Acquisition setting not verified consistently across these specimens. |
| Statistical inference and population prevalence | NOT APPLICABLE | Four selected historic references are not an independent representative sample. |
| QC figure and conceptual figures | PASSED | PNG/SVG produced from observed QC or explicitly labelled biological schema. |
| Six clean notebooks | PASSED | Valid notebook files with reusable-module code and no stored outputs. |
| Standalone report | PASSED | Editable LaTeX source, BibTeX bibliography, build script and PDF distinguish completed QC from pending analysis. |
| Automated code tests | PASSED | Four tests cover manifest validation, FASTA QC, caller parsing, Wilson calculation and plot creation. |
| Public release readiness | FAILED | Major genomic screening outputs and independent verification are missing. Do not claim completed AMR/virulence findings. |

**Specific completion path:** run AMRFinderPlus with a recorded database version in a supported environment, validate reference coverage for target genes, inspect native output, perform typing with dedicated methods if desired, and seek authentic phenotype and epidemiological metadata before making those comparisons. Rebuild the report and audit after new results are verified.

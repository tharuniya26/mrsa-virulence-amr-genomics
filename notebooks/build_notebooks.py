"""Regenerate six clean notebooks from short, reusable-module examples."""
from pathlib import Path
import nbformat as nbf

root = Path(__file__).resolve().parent
items = [
    ("01_genome_quality_control", "Inspect assembly QC", "Review the four downloaded NCBI RefSeq assemblies. Bounds are exploratory and specific to this reference cohort.",
     "from pathlib import Path\nimport pandas as pd\nfrom src.genome_qc import run\nfrom src.visualization import qc_figure\nrun(Path('data/metadata/genome_manifest.csv'), Path('data/raw'), Path('results/genome_qc.csv'))\nqc_figure(Path('results/genome_qc.csv'), Path('figures'))\npd.read_csv('results/genome_qc.csv')",
     "Interpretation: these are assembly properties only. See [QC figure](../figures/genome_qc.png) and [methods](../docs/methodology.md)."),
    ("02_amr_gene_analysis", "AMR screening status", "NCBI AMRFinderPlus is the planned caller. No marker results are inferred from the strain names.",
     "from pathlib import Path\nimport pandas as pd\np = Path('results/amr_gene_calls.csv')\npd.read_csv(p) if p.exists() else 'Pending: run python -m src.amr_analysis in a supported environment'",
     "Review the native TSVs and database version before reporting mecA, mecC or tet-family findings. No susceptibility inference follows from an isolated call."),
    ("03_virulence_gene_analysis", "Virulence screening status", "Positive VIRULENCE entries will be extracted from the same AMRFinderPlus output; database coverage must be checked.",
     "from pathlib import Path\nimport pandas as pd\np = Path('results/virulence_gene_calls.csv')\npd.read_csv(p) if p.exists() else 'Pending: run python -m src.virulence_analysis after AMRFinderPlus'",
     "A lukS-PV or lukF-PV call does not demonstrate active PVL production. A missing call is not a validated negative without reference coverage."),
    ("04_comparative_genomics", "Compare supported data", "Join metadata and QC; marker fields remain explicitly unassessed until caller output exists.",
     "from pathlib import Path\nimport pandas as pd\nfrom src.comparative_analysis import run\nrun(Path('data/metadata/genome_manifest.csv'), Path('results'))\npd.read_csv('results/comparative_genomics_summary.csv')[['assembly_accession','qc_status','amr_assessment','virulence_assessment']]",
     "No community versus healthcare, sequence type or phenotype comparison is supported by the verified metadata."),
    ("05_statistical_analysis", "Descriptive statistics", "Count selected and QC-pass assemblies; avoid inferential tests on this four-genome convenience cohort.",
     "from pathlib import Path\nfrom src.statistical_analysis import run, wilson\nrun(Path('results/genome_qc.csv'), Path('results/descriptive_summary.txt'))\nprint(Path('results/descriptive_summary.txt').read_text())",
     "Wilson intervals are available for future fully assessed binary outcomes, but no marker frequency or interval is reported here."),
    ("06_results_interpretation", "Interpret verified findings", "The completed observation is assembly-level QC. Marker and clinical claims remain pending.",
     "import pandas as pd\nqc = pd.read_csv('results/genome_qc.csv')\nqc[['assembly_accession','assembly_length_bp','contig_count','n50_bp','qc_status']]",
     "Four of four assemblies passed an exploratory FASTA screen. This does not establish completeness, absence of contamination, resistance, virulence or clinical outcome. See [limitations](../docs/limitations.md)."),
]
for name, title, context, code, interpretation in items:
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        nbf.v4.new_markdown_cell(f"# {title}\n\n**Objective and context.** {context}\n\n**Input.** Files in `data/metadata/`, `data/raw/` or `results/` as applicable. Run from the repository root."),
        nbf.v4.new_code_cell(code),
        nbf.v4.new_markdown_cell(f"**Biological interpretation and limitations.** {interpretation}\n\n**Output.** See `results/` and `figures/` where available."),
    ]
    notebook.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}
    nbf.write(notebook, root / f"{name}.ipynb")

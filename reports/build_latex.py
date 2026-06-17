"""Compile the report with pdflatex and bibtex, without latexmk/Perl."""
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
stem = "mrsa_genomic_analysis"
for command in (["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"],
                ["bibtex", stem],
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"],
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"]):
    print("Running:", " ".join(command), flush=True)
    result = subprocess.run(command, cwd=here, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"LaTeX build failed during {' '.join(command)}:\n" + "\n".join(result.stdout.splitlines()[-35:]))
print(here / f"{stem}.pdf")

"""Create original, literature-grounded conceptual diagrams."""
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["svg.hashsalt"] = "mrsa-genomics"


def _save_svg(fig, path: Path, **kwargs) -> None:
    fig.savefig(path, metadata={"Date": None}, **kwargs)
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def box(ax, x, y, label, color):
    ax.text(x, y, label, ha="center", va="center", fontsize=9,
            bbox={"boxstyle": "round,pad=0.45", "facecolor": color, "edgecolor": "#34495e"})


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#34495e"})


def run(out=Path("figures")):
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 2.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 2); ax.axis("off")
    labels = ["NCBI public\nassemblies", "Download\n+ provenance", "FASTA QC", "AMR / virulence\nscreening", "Marker comparison\n+ interpretation"]
    for i, label in enumerate(labels):
        box(ax, 1 + 2*i, 1, label, "#dceaf2" if i < 3 else "#fff0d9")
        if i: arrow(ax, 2*i-.4, 1, 2*i+.45, 1)
    ax.text(5, .16, "Blue: executed   |   Amber: pending validated screening", ha="center", fontsize=9)
    fig.savefig(out / "workflow.png", dpi=220, bbox_inches="tight")
    _save_svg(fig, out / "workflow.svg", dpi=220, bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5)); ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    box(ax, 1.5, 3.7, "mecA → PBP2a", "#dceaf2"); box(ax, 5, 3.7, "Lower affinity for many β-lactams", "#e8f2de"); arrow(ax, 2.7, 3.7, 3.4, 3.7)
    box(ax, 1.5, 2.5, "Tetracycline → 30S ribosome", "#dceaf2"); box(ax, 6.1, 2.5, "Tet(K): efflux   •   Tet(M): ribosome protection", "#e8f2de"); arrow(ax, 3.0, 2.5, 3.55, 2.5)
    box(ax, 1.5, 1.3, "lukS-PV + lukF-PV", "#dceaf2"); box(ax, 6.1, 1.3, "PVL pore formation in susceptible leukocytes", "#e8f2de"); arrow(ax, 2.8, 1.3, 3.4, 1.3)
    ax.text(5, .32, "Conceptual mechanisms; gene detection alone does not establish phenotype or toxin production.", ha="center", fontsize=9)
    fig.savefig(out / "molecular_mechanisms.png", dpi=220, bbox_inches="tight")
    _save_svg(fig, out / "molecular_mechanisms.svg", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__": run()

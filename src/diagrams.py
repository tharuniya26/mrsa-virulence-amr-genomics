"""Create original, literature-grounded conceptual diagrams."""
from pathlib import Path
import matplotlib.pyplot as plt


def box(ax, x, y, label, color):
    ax.text(x, y, label, ha="center", va="center", fontsize=9,
            bbox={"boxstyle": "round,pad=0.45", "facecolor": color, "edgecolor": "#34495e"})


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#34495e"})


def run(out=Path("figures")):
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 2.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 2); ax.axis("off")
    labels = ["NCBI public\nassemblies", "Download\n+ provenance", "FASTA QC", "AMR / virulence\nscreening", "Comparison\n+ interpretation"]
    for i, label in enumerate(labels):
        box(ax, 1 + 2*i, 1, label, "#dceaf2" if i < 3 else "#fff0d9")
        if i: arrow(ax, 2*i-.4, 1, 2*i+.45, 1)
    ax.text(5, .16, "Blue: executed   |   Amber: pending validated screening", ha="center", fontsize=9)
    for ext in ("svg", "png"): fig.savefig(out/f"workflow.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5)); ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    box(ax, 1.5, 3.7, "mecA → PBP2a", "#dceaf2"); box(ax, 5, 3.7, "Lower affinity for many β-lactams", "#e8f2de"); arrow(ax, 2.7, 3.7, 3.4, 3.7)
    box(ax, 1.5, 2.5, "Tetracycline → 30S ribosome", "#dceaf2"); box(ax, 6.1, 2.5, "Tet(K): efflux   •   Tet(M): ribosome protection", "#e8f2de"); arrow(ax, 3.0, 2.5, 3.55, 2.5)
    box(ax, 1.5, 1.3, "lukS-PV + lukF-PV", "#dceaf2"); box(ax, 6.1, 1.3, "PVL pore formation in susceptible leukocytes", "#e8f2de"); arrow(ax, 2.8, 1.3, 3.4, 1.3)
    ax.text(5, .32, "Conceptual mechanisms; gene detection alone does not establish phenotype or toxin production.", ha="center", fontsize=9)
    for ext in ("svg", "png"): fig.savefig(out/f"molecular_mechanisms.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__": run()

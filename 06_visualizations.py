import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np
import os

PALETTE = {
    "bg": "#F3EEFF",
    "panel": "#DCE8FF",
    "white": "#FFFFFF",
    "ink": "#241A43",
    "muted": "#6F688F",
    "line": "#D8D2E8",
    "dots": "#D9D0EC",
    "lavender": "#C9B7FF",
    "lavender_light": "#EEE8FF",
    "blue": "#5D8FEF",
    "blue_light": "#E7EEFF",
    "pink": "#FF4F89",
    "pink_light": "#FFE5EE",
    "red": "#E53935",
    "gold": "#FFC83D",
    "gold_light": "#FFF2C8",
    "green": "#32A85B",
    "green_light": "#E3F6E7",
    "violet": "#895EC7",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": PALETTE["ink"],
    "axes.labelcolor": PALETTE["ink"],
    "xtick.color": PALETTE["ink"],
    "ytick.color": PALETTE["ink"],
    "axes.titlecolor": PALETTE["ink"],
    "savefig.facecolor": PALETTE["bg"],
})

def dotted_background(fig):
    fig.patch.set_facecolor(PALETTE["bg"])
    for y in np.arange(0.015, 0.99, 0.035):
        for x in np.arange(0.012, 0.99, 0.025):
            fig.add_artist(Circle(
                (x, y), 0.00105, transform=fig.transFigure,
                facecolor=PALETTE["dots"], edgecolor="none", zorder=0
            ))

def add_card(fig, bounds, facecolor=PALETTE["white"], edgecolor=PALETTE["ink"],
             linewidth=2.2, shadow=True, linestyle="-"):
    x, y, width, height = bounds
    boxstyle = "round,pad=0.006,rounding_size=0.018"
    if shadow:
        fig.add_artist(FancyBboxPatch(
            (x + 0.008, y - 0.012), width, height,
            boxstyle=boxstyle, transform=fig.transFigure,
            facecolor=PALETTE["ink"], edgecolor=PALETTE["ink"],
            linewidth=0, zorder=1
        ))
    fig.add_artist(FancyBboxPatch(
        (x, y), width, height, boxstyle=boxstyle,
        transform=fig.transFigure, facecolor=facecolor,
        edgecolor=edgecolor, linewidth=linewidth,
        linestyle=linestyle, zorder=1.2
    ))

def page(title, figsize=(14, 8)):
    fig = plt.figure(figsize=figsize)
    dotted_background(fig)
    fig.text(
        0.065, 0.93, title, ha="left", va="center",
        fontsize=22, fontweight="bold", color=PALETTE["ink"]
    )
    return fig

def plot_panel(fig, bounds, facecolor=PALETTE["white"]):
    add_card(fig, bounds, facecolor=facecolor)
    x, y, width, height = bounds
    ax = fig.add_axes([
        x + 0.055, y + 0.095, width - 0.11, height - 0.17
    ], zorder=3)
    ax.patch.set_alpha(0)
    ax.tick_params(colors=PALETTE["ink"], labelsize=9.5, length=0, pad=7)
    for spine in ax.spines.values():
        spine.set_color(PALETTE["line"])
        spine.set_linewidth(1.1)
    ax.grid(True, color=PALETTE["line"], linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    return ax

def add_pill(fig, x, y, width, label, facecolor, fontsize=9):
    height = 0.052
    fig.add_artist(FancyBboxPatch(
        (x, y), width, height, transform=fig.transFigure,
        boxstyle="round,pad=0.006,rounding_size=0.018",
        facecolor=facecolor, edgecolor=PALETTE["ink"],
        linewidth=1.6, zorder=2
    ))
    fig.text(
        x + width / 2, y + height / 2, label,
        ha="center", va="center", fontsize=fontsize,
        fontweight="bold", color=PALETTE["ink"], zorder=3
    )

def save_fig(name, fig):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "visualizations", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(
        path, dpi=180, bbox_inches="tight",
        facecolor=PALETTE["bg"], pad_inches=0.15
    )
    plt.close(fig)
    print(f"[OK] Saved: visualizations/{name}.png")

def classical_complexity(bits):
    ln_n = bits * np.log(2)
    ln_ln_n = np.log(ln_n)
    c = (64 / 9) ** (1 / 3)
    return np.exp(c * (ln_n ** (1 / 3)) * (ln_ln_n ** (2 / 3)))

def quantum_complexity(bits):
    return bits ** 3

def plot_complexity_comparison():
    fig = page("Factoring Complexity: Asymptotic Growth Shapes")
    ax = plot_panel(fig, (0.055, 0.17, 0.89, 0.70))

    bits = np.linspace(64, 4096, 100)
    classical = [classical_complexity(b) for b in bits]
    quantum = [quantum_complexity(b) for b in bits]

    ax.semilogy(
        bits, classical, color=PALETTE["pink"], linewidth=3.2,
        label="GNFS asymptotic expression"
    )
    ax.semilogy(
        bits, quantum, color=PALETTE["blue"], linewidth=3.2,
        label="Shor polynomial proxy"
    )
    ax.axvline(
        x=2048, color=PALETTE["ink"], linestyle=":",
        linewidth=1.8, alpha=0.7
    )
    ax.text(
        2100, 1e20, "RSA-2048", color=PALETTE["ink"],
        fontsize=9.5, fontweight="bold",
        bbox={"boxstyle": "round,pad=0.32", "facecolor": PALETTE["gold"],
              "edgecolor": PALETTE["ink"], "linewidth": 1.2}
    )
    ax.set_xlabel("Key Size (bits)", fontsize=11, labelpad=8)
    ax.set_ylabel("Illustrative asymptotic expression (log scale)", fontsize=10, labelpad=8)
    ax.set_xlim(64, 4096)
    ax.set_ylim(1e3, 1e100)
    legend = ax.legend(
        fontsize=9.5, loc="upper left", frameon=True,
        facecolor=PALETTE["lavender_light"], edgecolor=PALETTE["ink"],
        fancybox=True, framealpha=1, borderpad=0.8
    )
    for text in legend.get_texts():
        text.set_color(PALETTE["ink"])
    fig.text(
        0.5, 0.075,
        "Constants, circuit costs, and hardware are omitted; curves are not wall-clock estimates.",
        ha="center", va="center", fontsize=9, color=PALETTE["muted"],
        bbox={"boxstyle": "round,pad=0.45", "facecolor": PALETTE["white"],
              "edgecolor": PALETTE["ink"], "linewidth": 1.1}
    )
    save_fig("01_complexity_comparison", fig)

def plot_speedup():
    fig = page("Asymptotic comparison")
    add_card(fig, (0.06, 0.39, 0.415, 0.37), facecolor=PALETTE["white"])
    add_card(fig, (0.525, 0.39, 0.415, 0.37), facecolor=PALETTE["panel"])
    add_card(
        fig, (0.06, 0.13, 0.88, 0.17), facecolor=PALETTE["lavender_light"],
        linestyle=(0, (5, 4))
    )

    add_pill(fig, 0.10, 0.68, 0.15, "CLASSICAL", PALETTE["lavender"])
    fig.text(
        0.10, 0.60, "Classical factoring", fontsize=17,
        fontweight="bold", color=PALETTE["ink"]
    )
    fig.text(
        0.10, 0.51, "GNFS: sub-exponential in the\nmodulus bit length",
        fontsize=12, color=PALETTE["muted"], linespacing=1.5
    )

    add_pill(fig, 0.565, 0.68, 0.14, "QUANTUM", PALETTE["gold"])
    fig.text(
        0.565, 0.60, "Quantum factoring", fontsize=17,
        fontweight="bold", color=PALETTE["ink"]
    )
    fig.text(
        0.565, 0.51, "Shor: polynomial in the\nmodulus bit length",
        fontsize=12, color=PALETTE["muted"], linespacing=1.5
    )

    fig.text(
        0.10, 0.215,
        "These complexity classes do not give a practical speedup ratio or attack date.\n"
        "A real attack also needs a sufficiently large, fault-tolerant quantum computer.",
        fontsize=10.5, color=PALETTE["ink"], linespacing=1.45, va="center"
    )
    save_fig("02_quantum_speedup", fig)

def plot_timeline():
    fig = page("PQC and Research Milestones (Not a Q-Day Forecast)")
    ax = plot_panel(fig, (0.055, 0.16, 0.89, 0.71), facecolor=PALETTE["white"])

    events = [
        (1994, "Shor publishes\nfactoring algorithm", "theory", 0.78),
        (2001, "First small-scale\nquantum factoring demo", "milestone", 0.24),
        (2024, "NIST publishes\nFIPS 203–205", "standard", 0.78),
        (2025, "SP 800-227 final;\nHQC selected", "standard", 0.24),
        (2035, "NIST transition\npolicy target", "policy", 0.78),
    ]
    colors = {
        "theory": PALETTE["blue"],
        "milestone": PALETTE["green"],
        "standard": PALETTE["violet"],
        "policy": PALETTE["gold"],
    }
    legend_handles = [
        mpatches.Patch(facecolor=colors["theory"], edgecolor=PALETTE["ink"], label="Theory"),
        mpatches.Patch(facecolor=colors["milestone"], edgecolor=PALETTE["ink"], label="Research milestone"),
        mpatches.Patch(facecolor=colors["standard"], edgecolor=PALETTE["ink"], label="Standardization"),
        mpatches.Patch(facecolor=colors["policy"], edgecolor=PALETTE["ink"], label="Policy target"),
    ]
    legend = fig.legend(
        handles=legend_handles, loc="upper center",
        bbox_to_anchor=(0.5, 0.855), ncol=4,
        frameon=False, fontsize=9
    )
    for label in legend.get_texts():
        label.set_color(PALETTE["ink"])

    marker_offsets = {2024: 0.055, 2025: -0.055}

    ax.plot(
        [1990, 2038], [0.5, 0.5], color=PALETTE["ink"],
        linewidth=2.5, solid_capstyle="round", zorder=1
    )
    for year, label, event_type, label_y in events:
        color = colors[event_type]
        marker_y = 0.5 + marker_offsets.get(year, 0)
        ax.plot(
            [year, year], [marker_y, label_y],
            color=color, linewidth=1.6, alpha=0.8, zorder=2
        )
        ax.scatter(
            year, marker_y, s=150, color=color, edgecolors=PALETTE["ink"],
            linewidths=1.5, zorder=4
        )
        ax.annotate(
            label, xy=(year, marker_y), xytext=(year, label_y),
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=PALETTE["ink"],
            bbox={"boxstyle": "round,pad=0.45", "facecolor": PALETTE["white"],
                  "edgecolor": PALETTE["ink"], "linewidth": 1.2},
            arrowprops={"arrowstyle": "-", "color": color, "linewidth": 1.4},
            zorder=5
        )

    ax.set_xlim(1990, 2038)
    ax.set_ylim(0.05, 0.95)
    ax.set_xticks([1990, 2000, 2010, 2020, 2030])
    ax.set_yticks([])
    ax.set_xlabel("Year", fontsize=10.5, labelpad=8)
    ax.grid(axis="x", color=PALETTE["line"], linewidth=0.8, alpha=0.8)
    ax.grid(axis="y", visible=False)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)

    save_fig("03_threat_timeline", fig)

def plot_algorithm_comparison():
    fig = page("Algorithm Families and NIST Standardization Status")
    rows = [
        (
            "Quantum-vulnerable public key",
            "RSA, Diffie–Hellman, ECDSA",
            "Shor threatens these in principle on a sufficiently capable fault-tolerant computer.",
            PALETTE["pink_light"], PALETTE["red"]
        ),
        (
            "Final NIST PQC standards",
            "ML-KEM (FIPS 203) · ML-DSA (FIPS 204) · SLH-DSA (FIPS 205)",
            "Published in 2024; designed to resist known classical and quantum attacks.",
            PALETTE["green_light"], PALETTE["green"]
        ),
        (
            "Selected; standards in development",
            "FN-DSA / Falcon (FIPS 206) · HQC (FIPS 207)",
            "Selected by NIST; selection is not the same as a final standard.",
            PALETTE["lavender_light"], PALETTE["violet"]
        ),
    ]
    row_positions = [0.64, 0.405, 0.17]
    for (heading, algorithms, note, fill, accent), y in zip(rows, row_positions):
        add_card(fig, (0.06, y, 0.88, 0.19), facecolor=fill)
        fig.add_artist(FancyBboxPatch(
            (0.078, y + 0.035), 0.012, 0.12,
            transform=fig.transFigure,
            boxstyle="round,pad=0.003,rounding_size=0.006",
            facecolor=accent, edgecolor=accent, linewidth=0, zorder=2
        ))
        fig.text(
            0.112, y + 0.14, heading,
            fontsize=12.5, fontweight="bold", color=PALETTE["ink"]
        )
        fig.text(
            0.112, y + 0.088, algorithms,
            fontsize=10.5, fontweight="bold", color=PALETTE["ink"]
        )
        fig.text(
            0.112, y + 0.038, note,
            fontsize=9.1, color=PALETTE["muted"]
        )
    save_fig("04_algorithm_comparison", fig)

def plot_qubit_progress():
    fig = page("One Model-Dependent Estimate for RSA-2048")
    add_card(fig, (0.06, 0.18, 0.88, 0.68), facecolor=PALETTE["panel"])
    fig.text(
        0.12, 0.75, "Gidney & Ekerå (2021)",
        fontsize=13, fontweight="bold", color=PALETTE["ink"]
    )
    ax = fig.add_axes([0.13, 0.38, 0.78, 0.30], zorder=3)
    ax.patch.set_alpha(0)
    ax.barh(
        [0], [20], height=0.42, color=PALETTE["gold"],
        edgecolor=PALETTE["ink"], linewidth=1.8, zorder=3
    )
    ax.text(
        10, 0, "20 million physical qubits",
        va="center", ha="center", color=PALETTE["ink"],
        fontsize=12, fontweight="bold", zorder=4
    )
    ax.set_xlim(0, 25)
    ax.set_ylim(-0.65, 0.65)
    ax.set_yticks([])
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_xlabel("Estimated physical qubits (millions)", fontsize=10.5, labelpad=8)
    ax.tick_params(colors=PALETTE["ink"], labelsize=9.5, length=0, pad=7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color=PALETTE["line"], linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)
    fig.text(
        0.12, 0.255,
        "The paper modeled an 8-hour runtime. This is not a current capability, universal threshold, or forecast.\n"
        "Logical and physical qubit counts are different quantities.",
        fontsize=9.5, color=PALETTE["muted"], linespacing=1.4
    )
    save_fig("05_qubit_progress", fig)

if __name__ == "__main__":
    print("=" * 60)
    print("  GENERATING QUANTUM THREAT VISUALIZATIONS")
    print("=" * 60)

    plot_complexity_comparison()
    plot_speedup()
    plot_timeline()
    plot_algorithm_comparison()
    plot_qubit_progress()

    print("\n" + "=" * 60)
    print("[OK] All visualizations saved to: visualizations/")
    print("=" * 60)


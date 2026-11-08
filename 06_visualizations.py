"""
Publication-quality figures for the Quantum-crypto project.

Every figure is self-contained: a title, a one-line subtitle, the plot, and a
notes/sources line, so it can be read without the surrounding README. Curves
are computed from the formulas stated in the notes; dated points come from the
cited primary sources.

Output: visualizations/*.png (300 dpi, 7.2 in wide = double-column width).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visualizations")
DPI = 300
WIDTH = 7.2  # inches

# Colour roles. Categorical hues were checked for colour-vision-deficiency
# separation; status hues are used only together with a glyph and a text label.
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e6e5df"
AXIS = "#b9b8ae"
BAND = "#f4f3ef"

CLASSICAL = "#2a78d6"  # blue: classical cryptanalysis
QUANTUM = "#eb6834"    # orange: quantum cryptanalysis
STANDARD = "#1baf7a"   # aqua: standards and policy

GOOD = "#0ca30c"
WARNING = "#e19a00"
CRITICAL = "#d03b3b"


def _pick_font():
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"):
        if name in available:
            return name
    return "DejaVu Sans"


FONT = _pick_font()

plt.rcParams.update({
    "font.family": FONT,
    "font.size": 8,
    "mathtext.fontset": "custom" if FONT != "DejaVu Sans" else "dejavusans",
    "mathtext.rm": FONT,
    "mathtext.it": f"{FONT}:italic",
    "mathtext.bf": f"{FONT}:bold",
    "mathtext.sf": FONT,
    "mathtext.cal": FONT,
    "mathtext.tt": "DejaVu Sans Mono",
    "text.color": INK,
    "axes.edgecolor": AXIS,
    "axes.linewidth": 0.7,
    "axes.labelcolor": INK_2,
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "xtick.color": AXIS,
    "ytick.color": AXIS,
    "xtick.labelcolor": INK_2,
    "ytick.labelcolor": INK_2,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "legend.fontsize": 7.5,
    "legend.frameon": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def new_figure(height, title, subtitle):
    """Create a figure with a left-aligned title block (positions in inches)."""
    fig = plt.figure(figsize=(WIDTH, height))
    left = 0.30 / WIDTH
    fig.text(left, 1 - 0.24 / height, title, ha="left", va="baseline",
             fontsize=11, fontweight="bold", color=INK)
    fig.text(left, 1 - 0.44 / height, subtitle, ha="left", va="baseline",
             fontsize=8, color=INK_2)
    return fig


def add_axes(fig, left, bottom, right, top):
    """Add axes using margins in inches from each figure edge."""
    w, h = fig.get_size_inches()
    return fig.add_axes([left / w, bottom / h, 1 - (left + right) / w,
                         1 - (bottom + top) / h])


def add_notes(fig, lines):
    """Notes and sources, anchored to the bottom-left corner."""
    _, h = fig.get_size_inches()
    fig.text(0.30 / WIDTH, 0.14 / h, "\n".join(lines), ha="left", va="bottom",
             fontsize=6.3, color=MUTED, linespacing=1.45)


def style_axes(ax, grid_axis="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"[OK] Saved: visualizations/{name}.png")


# ---------------------------------------------------------------------------
# Cost models (heuristic, o(1) terms set to zero)
# ---------------------------------------------------------------------------

LN2 = np.log(2)


def l_notation_bits(n_bits, alpha, c):
    """log2 of L_N[alpha, c] = exp(c (ln N)^alpha (ln ln N)^(1-alpha))."""
    ln_n = np.asarray(n_bits, dtype=float) * LN2
    return c * ln_n ** alpha * np.log(ln_n) ** (1 - alpha) / LN2


def gnfs_bits(n_bits):
    return l_notation_bits(n_bits, 1 / 3, (64 / 9) ** (1 / 3))


def quadratic_sieve_bits(n_bits):
    return l_notation_bits(n_bits, 1 / 2, 1.0)


def shor_gate_bits(n_bits):
    """log2(n^3): gate count of schoolbook modular exponentiation."""
    return 3 * np.log2(n_bits)


# NIST SP 800-57 Part 1 Rev. 5, Table 2: RSA modulus size -> security strength.
NIST_STRENGTH = [(1024, 80), (2048, 112), (3072, 128), (7680, 192), (15360, 256)]

# Gidney & Ekera (2021): 0.3 n^3 + 0.0005 n^3 lg n Toffoli gates.
GE_TOFFOLI_2048 = 0.3 * 2048 ** 3 + 0.0005 * 2048 ** 3 * np.log2(2048)


# ---------------------------------------------------------------------------
# Figure 1: cost exponent versus modulus size
# ---------------------------------------------------------------------------

def plot_complexity_comparison():
    fig = new_figure(
        4.6,
        "Classical and quantum factoring costs scale differently with key size",
        "Heuristic cost exponent of the best classical (GNFS) and quantum (Shor) "
        "factoring algorithms, compared with NIST security-strength ratings",
    )
    ax = add_axes(fig, left=0.80, bottom=1.02, right=1.55, top=0.72)
    style_axes(ax)

    n = np.geomspace(512, 16384, 400)
    ax.plot(n, gnfs_bits(n), color=CLASSICAL, lw=1.9, solid_capstyle="round",
            zorder=3)
    ax.plot(n, shor_gate_bits(n), color=QUANTUM, lw=1.9, solid_capstyle="round",
            zorder=3)

    # Calibration points
    xs, ys = zip(*NIST_STRENGTH)
    ax.scatter(xs, ys, s=26, facecolor="white", edgecolor=INK, linewidth=1.0,
               zorder=5)
    for x, y in NIST_STRENGTH:
        label = "≤ 80" if x == 1024 else f"{y}"
        ax.annotate(label, (x, y), xytext=(6, -3), textcoords="offset points",
                    ha="left", va="top", fontsize=7, color=INK)

    ge_bits = np.log2(GE_TOFFOLI_2048)
    ax.scatter([2048], [ge_bits], s=30, marker="D", facecolor=QUANTUM,
               edgecolor="white", linewidth=0.8, zorder=5)
    ax.annotate(r"Gidney & Ekerå (2021): $2.6\times10^{9}$ Toffoli gates "
                r"($\approx 2^{31}$)",
                (2048, ge_bits), xytext=(7, -4), textcoords="offset points",
                ha="left", va="top", fontsize=6.8, color=INK_2)

    # Largest RSA challenge numbers factored so far sit far left of 2048.
    ax.axvline(829, color=MUTED, lw=0.8, ls=(0, (2.5, 2.5)), zorder=1)
    ax.text(829 * 1.03, 283, "RSA-250 (829 bits)\nfactored with GNFS, 2020",
            ha="left", va="top", fontsize=6.8, color=INK_2, linespacing=1.3)

    # Direct labels at the right end of each curve
    x_end = 16384
    ax.text(x_end * 1.04, gnfs_bits(x_end), "GNFS (classical)",
            ha="left", va="center", fontsize=8, fontweight="bold",
            color=INK)
    ax.text(x_end * 1.04, gnfs_bits(x_end) - 13,
            r"$L_N[\,1/3,\ (64/9)^{1/3}\,]$",
            ha="left", va="center", fontsize=7.3, color=INK_2)
    ax.text(x_end * 1.04, shor_gate_bits(x_end) + 6, "Shor (quantum)",
            ha="left", va="center", fontsize=8, fontweight="bold",
            color=INK)
    ax.text(x_end * 1.04, shor_gate_bits(x_end) - 7,
            r"$\propto n^{3}$ logical gates",
            ha="left", va="center", fontsize=7.3, color=INK_2)

    ax.set_xscale("log", base=2)
    ticks = [512, 1024, 2048, 4096, 8192, 16384]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_xlim(512, 16384)
    ax.set_ylim(0, 290)
    ax.yaxis.set_major_locator(FixedLocator([0, 64, 128, 192, 256]))
    ax.set_xlabel(r"RSA modulus size $n$ (bits, log scale)", labelpad=5)
    ax.set_ylabel(r"Cost exponent, $\log_2$(operations)", labelpad=5)

    legend = [
        Line2D([], [], ls="", marker="o", ms=5, mfc="white", mec=INK, mew=1.0,
               label="NIST SP 800-57 security strength (bits)"),
        Line2D([], [], ls="", marker="D", ms=4.6, mfc=QUANTUM, mec="white",
               mew=0.8, label="Published Shor circuit, RSA-2048"),
    ]
    ax.legend(handles=legend, loc="lower right", bbox_to_anchor=(1.0, 0.25),
              handletextpad=0.4, borderaxespad=0.2, labelcolor=INK_2)

    add_notes(fig, [
        r"Notes: GNFS curve is $L_N[1/3,(64/9)^{1/3}]$ with the $o(1)$ term set to 0, "
        "in elementary operations. Shor curve is $3\\log_2 n$ (schoolbook modular "
        "exponentiation), in logical gates,",
        "excluding error-correction overhead. The units differ: compare growth "
        "rates, not wall-clock time.",
        "Sources: NIST SP 800-57 Pt. 1 Rev. 5, Table 2; Gidney & Ekerå, Quantum 5, "
        "433 (2021); Boudot et al., RSA-250 factorization (2020).",
    ])
    save(fig, "01_complexity_comparison")


# ---------------------------------------------------------------------------
# Figure 2: algorithms on the L-notation scale
# ---------------------------------------------------------------------------

def plot_speedup():
    rows = [
        # name, model, alpha, L-notation label, log2 cost at n = 2048
        ("Shor's algorithm", "quantum", 0.0, r"$L_N[0,\,3]\propto n^{3}$",
         shor_gate_bits(2048)),
        ("General number field sieve", "classical", 1 / 3,
         r"$L_N[1/3,\,1.923]$", gnfs_bits(2048)),
        ("Quadratic sieve", "classical", 1 / 2, r"$L_N[1/2,\,1]$",
         quadratic_sieve_bits(2048)),
        ("Pollard's rho", "classical", 1.0, r"$L_N[1,\,1/4]=N^{1/4}$", 2048 / 4),
        ("Trial division", "classical", 1.0, r"$L_N[1,\,1/2]=N^{1/2}$", 2048 / 2),
    ]

    fig = new_figure(
        3.55,
        "Factoring algorithms on the L-notation scale",
        r"Each method's asymptotic class, from polynomial ($\alpha=0$) to "
        r"exponential ($\alpha=1$) in the size of $N$",
    )
    ax = add_axes(fig, left=2.05, bottom=0.92, right=1.20, top=0.95)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    ax.axvspan(0.0, 1.0, color=BAND, zorder=0, lw=0)
    for x in (0.0, 1.0):
        ax.axvline(x, color=AXIS, lw=0.8, zorder=1)

    y = np.arange(len(rows))[::-1]
    for yi, (name, model, alpha, label, cost) in zip(y, rows):
        color = QUANTUM if model == "quantum" else CLASSICAL
        ax.plot([0, alpha], [yi, yi], color=GRID, lw=0.8, zorder=1)
        ax.scatter(alpha, yi, s=44, color=color, edgecolor="white",
                   linewidth=1.0, zorder=4,
                   marker="D" if model == "quantum" else "o")
        right_side = alpha < 0.8
        ax.annotate(label, (alpha, yi), xytext=(8 if right_side else -8, 0),
                    textcoords="offset points",
                    ha="left" if right_side else "right", va="center",
                    fontsize=7.6, color=INK)
        # Row label and model, in the left margin
        ax.text(-0.075, yi + 0.12, name, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=8, fontweight="bold",
                color=INK)
        ax.text(-0.075, yi - 0.2, model, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=7, color=INK_2)
        # Cost column, in the right margin
        ax.text(1.07, yi, f"≈ 2$^{{{cost:.0f}}}$",
                transform=ax.get_yaxis_transform(), ha="left", va="center",
                fontsize=8, color=INK)

    ax.text(1.07, len(rows) - 0.35, "Cost at\n$n$ = 2,048",
            transform=ax.get_yaxis_transform(), ha="left", va="bottom",
            fontsize=7, color=INK_2, linespacing=1.25)
    for x, text, ha in ((0.0, "Polynomial", "center"),
                        (0.5, "Sub-exponential", "center"),
                        (1.0, "Exponential", "center")):
        ax.text(x, len(rows) - 0.35, text, ha=ha, va="bottom", fontsize=7.5,
                fontweight="bold", color=INK_2)

    ax.set_xlim(-0.06, 1.06)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks([])
    alpha_ticks = {0.0: "0", 1 / 3: "1/3", 1 / 2: "1/2", 1.0: "1"}
    ax.xaxis.set_major_locator(FixedLocator(list(alpha_ticks)))
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: min(alpha_ticks.items(), key=lambda kv: abs(kv[0] - v))[1]))
    ax.set_xlabel(r"Exponent $\alpha$ in $L_N[\alpha, c]$", labelpad=4)

    add_notes(fig, [
        r"Notes: $L_N[\alpha,c]=\exp\,[(c+o(1))\,(\ln N)^{\alpha}(\ln\ln N)^{1-\alpha}]$. "
        r"Costs at $n=2048$ set $o(1)=0$ and omit constants; Shor counts logical "
        r"gates ($n^3$), classical rows count operations.",
        "Pollard's rho and trial division costs assume a balanced RSA modulus "
        r"(smallest prime factor $\approx N^{1/2}$).",
    ])
    save(fig, "02_quantum_speedup")


# ---------------------------------------------------------------------------
# Figure 3: milestones
# ---------------------------------------------------------------------------

TODAY = 2026 + 10.3 / 12  # early November 2026


def plot_timeline():
    groups = [
        ("Cryptanalysis", [
            (1994.8, "Shor publishes the quantum factoring algorithm", QUANTUM, "D"),
            (2001.9, "15 factored on a 7-qubit NMR device", QUANTUM, "D"),
            (2020.2, "RSA-250 (829 bits) factored with GNFS", CLASSICAL, "o"),
            (2021.3, "RSA-2048 estimate: 20 M qubits, 8 h", QUANTUM, "D"),
            (2025.4, "RSA-2048 estimate: < 1 M qubits, < 1 week", QUANTUM, "D"),
        ]),
        ("NIST standardization", [
            (2016.97, "Call for post-quantum proposals", STANDARD, "s"),
            (2022.5, "First four algorithms selected", STANDARD, "s"),
            (2024.6, "FIPS 203, 204, 205 published", STANDARD, "s"),
            (2025.2, "HQC selected as backup KEM", STANDARD, "s"),
            (2025.7, "SP 800-227 (KEM guidance) final", STANDARD, "s"),
        ]),
        ("NIST transition (IR 8547 draft)", [
            (2030.0, "112-bit schemes (e.g., RSA-2048) deprecated after 2030", STANDARD, "s_open"),
            (2035.0, "Quantum-vulnerable public key disallowed after 2035", STANDARD, "s_open"),
        ]),
    ]

    n_rows = sum(len(events) + 1 for _, events in groups)
    height = 0.95 + 0.205 * n_rows + 0.75
    fig = new_figure(
        height,
        "Cryptanalysis, standardization, and policy milestones",
        "Dated events only. Policy dates are NIST transition targets, "
        "not forecasts of quantum capability",
    )
    ax = add_axes(fig, left=3.05, bottom=0.78, right=0.30, top=0.70)
    style_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)

    yi = n_rows - 1
    for group, events in groups:
        ax.text(-0.025, yi, group, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=8, fontweight="bold",
                color=INK)
        yi -= 1
        for year, label, color, marker in events:
            ax.plot([1990, year], [yi, yi], color=GRID, lw=0.6, zorder=1)
            hollow = marker.endswith("_open")
            ax.scatter(year, yi, s=34, marker=marker.replace("_open", ""),
                       facecolor="white" if hollow else color,
                       edgecolor=color if hollow else "white",
                       linewidth=1.2 if hollow else 0.8, zorder=4)
            ax.text(-0.025, yi, label, transform=ax.get_yaxis_transform(),
                    ha="right", va="center", fontsize=7.6, color=INK_2)
            future = year > TODAY
            ax.annotate(f"{int(year)}", (year, yi), xytext=(6 if future else -6, 0),
                        textcoords="offset points",
                        ha="left" if future else "right", va="center",
                        fontsize=7, color=INK, zorder=3,
                        bbox=dict(boxstyle="square,pad=0.15", lw=0,
                                  facecolor=BAND if future else "white"))
            yi -= 1

    ax.axvspan(TODAY, 2040, color=BAND, lw=0, zorder=0)
    ax.axvline(TODAY, color=MUTED, lw=0.8, ls=(0, (2.5, 2.5)), zorder=2)
    ax.text(TODAY + 0.4, n_rows - 0.55, "Nov 2026", ha="left", va="center",
            fontsize=7, color=INK_2)

    ax.set_xlim(1990, 2040)
    ax.set_ylim(-0.7, n_rows - 0.3)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(FixedLocator(range(1990, 2041, 10)))
    ax.set_xlabel("Year", labelpad=4)

    legend = [
        Line2D([], [], ls="", marker="D", ms=5, mfc=QUANTUM, mec="white",
               label="Quantum"),
        Line2D([], [], ls="", marker="o", ms=5.5, mfc=CLASSICAL, mec="white",
               label="Classical"),
        Line2D([], [], ls="", marker="s", ms=5, mfc=STANDARD, mec="white",
               label="Standard, published"),
        Line2D([], [], ls="", marker="s", ms=5, mfc="white", mec=STANDARD,
               mew=1.2, label="Draft policy target"),
    ]
    ax.legend(handles=legend, loc="lower left", bbox_to_anchor=(0.0, 1.0),
              ncol=4, handletextpad=0.3, columnspacing=1.2,
              borderaxespad=0.15, labelcolor=INK_2)

    add_notes(fig, [
        "Sources: Shor, FOCS (1994); Vandersypen et al., Nature 414, 883 (2001); "
        "Boudot et al. (2020); Gidney & Ekerå, Quantum 5, 433 (2021); "
        "Gidney, arXiv:2505.15917 (2025);",
        "NIST PQC project, FIPS 203–205, SP 800-227, and IR 8547 initial public "
        "draft (Nov 2024).",
    ])
    save(fig, "03_threat_timeline")


# ---------------------------------------------------------------------------
# Figure 4: algorithm families table
# ---------------------------------------------------------------------------

def plot_algorithm_comparison():
    groups = [
        ("Quantum-vulnerable public key (Shor's algorithm applies)", [
            ("RSA", "Integer factorization", "Encryption, signatures",
             "Vulnerable", "critical"),
            ("DH, DSA", "Finite-field discrete logarithm",
             "Key exchange, signatures", "Vulnerable", "critical"),
            ("ECDH, ECDSA, EdDSA", "Elliptic-curve discrete logarithm",
             "Key exchange, signatures", "Vulnerable", "critical"),
        ]),
        ("NIST post-quantum algorithms", [
            ("ML-KEM", "Module lattices", "Key encapsulation",
             "FIPS 203, final (2024)", "good"),
            ("ML-DSA", "Module lattices", "Digital signatures",
             "FIPS 204, final (2024)", "good"),
            ("SLH-DSA", "Hash functions (stateless)", "Digital signatures",
             "FIPS 205, final (2024)", "good"),
            ("FN-DSA (Falcon)", "NTRU lattices", "Digital signatures",
             "FIPS 206, in development", "warning"),
            ("HQC", "Quasi-cyclic codes", "Key encapsulation",
             "Selected 2025, in development", "warning"),
        ]),
    ]
    status_style = {
        "critical": dict(marker="X", s=40, facecolor=CRITICAL, edgecolor="white", linewidth=0.6),
        "good": dict(marker="o", s=34, facecolor=GOOD, edgecolor="white", linewidth=0.6),
        "warning": dict(marker="o", s=30, facecolor="white", edgecolor=WARNING, linewidth=1.4),
    }

    n_lines = sum(len(rows) + 1 for _, rows in groups) + 1
    row_h = 0.235
    height = 0.80 + row_h * n_lines + 0.62
    fig = new_figure(
        height,
        "Public-key algorithm families and NIST standardization status",
        "Shor's algorithm breaks the first group only on a large fault-tolerant "
        "quantum computer, which does not exist today",
    )
    ax = add_axes(fig, left=0.30, bottom=0.55, right=0.30, top=0.68)
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(-n_lines + 0.5, 0.5)

    cols = [0.0, 0.205, 0.475, 0.70]
    headers = ["Scheme", "Mathematical basis", "Use", "Status"]
    for x, header in zip(cols, headers):
        ax.text(x, 0, header, ha="left", va="center", fontsize=7.5,
                fontweight="bold", color=INK_2)
    ax.axhline(0.5, color=INK, lw=0.9)
    ax.axhline(-0.5, color=INK, lw=0.5)

    yi = -1
    for g_index, (group, rows) in enumerate(groups):
        if g_index:
            ax.axhline(yi + 0.5, color=GRID, lw=0.6)
        ax.text(0, yi, group, ha="left", va="center", fontsize=7.6,
                fontstyle="italic", color=INK_2)
        yi -= 1
        for scheme, basis, use, status, kind in rows:
            ax.text(cols[0] + 0.012, yi, scheme, ha="left", va="center",
                    fontsize=8, fontweight="bold", color=INK)
            ax.text(cols[1], yi, basis, ha="left", va="center", fontsize=7.8,
                    color=INK)
            ax.text(cols[2], yi, use, ha="left", va="center", fontsize=7.8,
                    color=INK)
            ax.scatter(cols[3] + 0.008, yi, zorder=3, **status_style[kind])
            ax.text(cols[3] + 0.026, yi, status, ha="left", va="center",
                    fontsize=7.8, color=INK)
            yi -= 1
    ax.axhline(yi + 0.5, color=INK, lw=0.9)

    add_notes(fig, [
        "Status checked November 2026; for updates see the NIST Post-Quantum "
        "Cryptography project (csrc.nist.gov/projects/post-quantum-cryptography).",
    ])
    save(fig, "04_algorithm_comparison")


# ---------------------------------------------------------------------------
# Figure 5: published RSA-2048 resource estimates
# ---------------------------------------------------------------------------

def plot_qubit_progress():
    fig = new_figure(
        4.35,
        "Published resource estimates for factoring RSA-2048",
        "Physical qubits versus runtime under the same hardware assumptions. "
        "These are engineering estimates, not forecasts",
    )
    ax = add_axes(fig, left=0.80, bottom=0.92, right=0.40, top=0.70)
    style_axes(ax, grid_axis=None)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e5, 2e8)
    ax.set_ylim(1, 1500)

    # Iso-lines of constant space-time volume (physical qubit-hours). The label
    # angle is measured in display space so it follows the drawn line.
    xs = np.geomspace(1e5, 2e8, 50)
    for volume in (1e7, 1e8, 1e9):
        ax.plot(xs, volume / xs, color=GRID, lw=0.8, zorder=1)
    p0, p1 = ax.transData.transform([(1e6, 10.0), (1e7, 1.0)])
    angle = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    for volume, x_label in ((1e7, 1.3e6), (1e8, 4.5e7), (1e9, 7e7)):
        exponent = int(np.log10(volume))
        ax.text(x_label, volume / x_label * 1.12,
                rf"$10^{{{exponent}}}$ qubit-hours", rotation=angle,
                rotation_mode="anchor", ha="left", va="bottom",
                fontsize=6.6, color=MUTED)

    estimates = [
        (2e7, 8, "Gidney & Ekerå (2021)", "20 million qubits, 8 hours"),
        (1e6, 168, "Gidney (2025)", "< 1 million qubits, < 1 week"),
    ]
    (x0, y0, *_), (x1, y1, *_) = estimates
    ax.annotate("", xy=(x1 * 1.25, y1 / 1.18), xytext=(x0 / 1.25, y0 * 1.18),
                arrowprops=dict(arrowstyle="-|>", color=INK_2, lw=0.9,
                                shrinkA=2, shrinkB=2, mutation_scale=8),
                zorder=2)
    ax.text(np.sqrt(x0 * x1) * 1.35, np.sqrt(y0 * y1) * 1.35,
            "> 20× fewer qubits,\n< 21× longer runtime",
            ha="left", va="bottom", fontsize=7, color=INK_2, linespacing=1.3)

    for x, y, who, what in estimates:
        ax.scatter(x, y, s=60, marker="D", facecolor=QUANTUM,
                   edgecolor="white", linewidth=1.0, zorder=4)
    ax.annotate(estimates[0][2], (x0, y0), xytext=(0, -11),
                textcoords="offset points", ha="center", va="top",
                fontsize=8, fontweight="bold", color=INK)
    ax.annotate(estimates[0][3], (x0, y0), xytext=(0, -22),
                textcoords="offset points", ha="center", va="top",
                fontsize=7.3, color=INK_2)
    ax.annotate(estimates[1][2], (x1, y1), xytext=(0, 20),
                textcoords="offset points", ha="center", va="bottom",
                fontsize=8, fontweight="bold", color=INK)
    ax.annotate(estimates[1][3] + " (upper bounds)", (x1, y1), xytext=(0, 9),
                textcoords="offset points", ha="center", va="bottom",
                fontsize=7.3, color=INK_2)

    ax.xaxis.set_major_locator(FixedLocator([1e5, 1e6, 1e7, 1e8]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: {1e5: "100 k", 1e6: "1 M", 1e7: "10 M", 1e8: "100 M"}[v]))
    hours = {1: "1 hour", 24: "1 day", 168: "1 week", 720: "1 month"}
    ax.yaxis.set_major_locator(FixedLocator(list(hours)))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: hours[int(round(v))]))
    for value in hours:
        ax.axhline(value, color=GRID, lw=0.6, zorder=0)
    ax.set_xlabel("Physical qubits (log scale)", labelpad=5)
    ax.set_ylabel("Runtime to factor one modulus (log scale)", labelpad=5)

    add_notes(fig, [
        "Notes: both estimates assume a surface-code architecture with "
        r"$10^{-3}$ physical gate error, 1 $\mu$s cycle time, and 10 $\mu$s control "
        "reaction time.",
        "The 2025 values are the paper's stated upper bounds. Grey diagonals mark "
        "constant physical qubit-hours.",
        "Sources: Gidney & Ekerå, Quantum 5, 433 (2021), arXiv:1905.09749; "
        "Gidney, arXiv:2505.15917 (2025).",
    ])
    save(fig, "05_qubit_progress")


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

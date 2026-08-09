"""Redraw of fig-notes-090: one-loop fermion-loop contribution to the phi
propagator in SUSY QM with P'(phi) = m phi + g phi^3.  Top: continuum value
6g int dp/2pi (-ip+m)/(p^2+m^2) ~ 3g.  Bottom: lattice (Wilson) value, which
tends to 6g as a -> 0 because the doubler also contributes."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
GREEN = "#009E73"
RED = "#D55E00"
INK = "0.15"


def loop_diagram(ax, cx, cy, r=0.34, leg=0.62):
    """Dashed scalar legs attached to a solid fermion loop."""
    ax.plot([cx - r - leg, cx - r], [cy, cy], color=INK, lw=1.3,
            ls=(0, (3.5, 2.5)), zorder=2)
    ax.plot([cx + r, cx + r + leg], [cy, cy], color=INK, lw=1.3,
            ls=(0, (3.5, 2.5)), zorder=2)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=BLUE, lw=1.5,
            zorder=3)


fig, ax = plt.subplots(figsize=(8.0, 3.6))
ax.axis("off")

y1, y2, y3 = 3.55, 1.85, 0.55  # row baselines

# ======================= row 1: continuum ================================
loop_diagram(ax, 1.05, y1)
ax.text(2.02, y1 - 0.02, r"$|_{\mathrm{continuum}}$", color=RED,
        fontsize=13, ha="left", va="center")
ax.text(3.20, y1,
        r"$=\ 6g\int_{-\pi/a}^{\pi/a}\frac{dp}{2\pi}\,"
        r"\frac{-ip+m}{p^2+m^2}"
        r"\ =\ \frac{6g}{\pi}\arctan\!\left(\frac{\pi}{2ma}\right)"
        r"\ \sim\ 3g+\mathcal{O}(ma)$",
        fontsize=12, ha="left", va="center", color=INK)

# green annotations, row 1
ax.annotate(r"$\psi_i$", xy=(0.87, y1 + 0.30), xytext=(0.45, y1 + 0.85),
            fontsize=11, color=GREEN, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9,
                            shrinkA=4, shrinkB=2))
ax.annotate(r"$\phi$", xy=(0.35, y1 - 0.06), xytext=(0.02, y1 - 0.70),
            fontsize=11, color=GREEN, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9,
                            shrinkA=4, shrinkB=2))
ax.annotate("vanishes by $p\\to -p$", xy=(5.45, y1 + 0.32),
            xytext=(5.35, y1 + 0.98), fontsize=9, color=GREEN,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9,
                            shrinkA=2, shrinkB=1))
ax.annotate("can cut off in other ways, but is finite anyway",
            xy=(3.90, y1 - 0.38), xytext=(4.65, y1 - 0.98), fontsize=9,
            color=GREEN, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9,
                            shrinkA=2, shrinkB=1))
ax.text(9.85, y1 + 0.95, r"$\psi_2=\bar{\psi}_1$ here", fontsize=10,
        color=GREEN, ha="right", va="center")

# ======================= row 2: lattice ==================================
loop_diagram(ax, 1.05, y2)
ax.text(2.02, y2 - 0.02, r"$|_{\mathrm{lattice}}$", color=RED,
        fontsize=13, ha="left", va="center")
ax.text(3.20, y2,
        r"$=\ \frac{6g}{L}\sum_{k=0}^{L-1}"
        r"\frac{-2i\sin(\pi k/L)\,e^{i\pi k/L}+m_W a}"
        r"{\sin^2(\pi k/L)+m_W^2 a^2}$",
        fontsize=12, ha="left", va="center", color=INK)
ax.annotate("", xy=(7.75, y2), xytext=(6.95, y2),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                            mutation_scale=12))
ax.text(7.35, y2 + 0.16, r"$a\to 0$", fontsize=10, ha="center",
        va="bottom", color=INK)
ax.text(7.95, y2, r"$6g$", fontsize=12, ha="left", va="center", color=INK)

# ======================= bottom line =====================================
ax.text(1.0, y3,
        r"where  $m_W a = ma + 2\sin^2\!\left(\frac{\pi k}{2L}\right)$"
        r"  due to Wilson term",
        fontsize=11, ha="left", va="center", color=INK)

ax.set_xlim(-0.1, 10.0)
ax.set_ylim(0.1, 4.75)

fig.savefig("../fig-redraw-090.pdf")
fig.savefig("../fig-redraw-090.png", dpi=200)
print("done 090")

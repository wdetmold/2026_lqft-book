"""Redraw of fig-notes-048: the step-scaling procedure for the running
Schroedinger-functional coupling.  Each row: a lattice of physical size L at
fixed (g_0,m_0) -- hence fixed spacing a_(i) -- is doubled to 2L, giving
Sigma(u, a_i/L).  Rows share the same physical L and the same u = gbar^2(L)
but different a; extrapolating a/L -> 0 yields sigma(u)."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import FancyArrowPatch

BLUE = "#0072B2"
GREEN = "#009E73"
LGREEN = "#e4f2e7"
ORANGE = "#D55E00"


def grid(ax, x0, y0, size, n):
    """lattice of physical extent `size` with n cells per side"""
    ax.add_patch(plt.Rectangle((x0, y0), size, size, facecolor=LGREEN,
                               edgecolor="none", zorder=1))
    for k in range(n + 1):
        u = k * size / n
        ax.plot([x0, x0 + size], [y0 + u, y0 + u], color=GREEN, lw=0.8,
                zorder=2)
        ax.plot([x0 + u, x0 + u], [y0, y0 + size], color=GREEN, lw=0.8,
                zorder=2)


def bracket(ax, x, y0, y1, label):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-[",
                                 mutation_scale=6, lw=1.0, color=BLUE,
                                 shrinkA=0, shrinkB=0))
    ax.text(x + 0.32, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=12, color=BLUE)


def harrow(ax, x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3,
                                mutation_scale=13, shrinkA=0, shrinkB=0))


fig, ax = plt.subplots(figsize=(8.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# ---- top row: coarse spacing a_(1) ---------------------------------------
grid(ax, 0.0, 5.4, 2.0, 4)
bracket(ax, 2.25, 5.4, 7.4, r"$L$")
ax.text(1.0, 5.05, r"$(g_0,m_0)_1 \rightarrow a_{(1)}$", ha="center",
        va="top", fontsize=10)

harrow(ax, 3.3, 4.7, 6.4)
ax.text(4.0, 6.72, "same $a_{(1)}$, since\nsame $(g_0,m_0)_1$",
        ha="center", va="bottom", fontsize=8.5)

grid(ax, 5.0, 4.4, 4.0, 8)
bracket(ax, 9.25, 4.4, 8.4, r"$2L$")

harrow(ax, 10.4, 11.2, 6.4)
ax.text(11.5, 6.4, r"$\Sigma(u,\,a_1/L)$", ha="left", va="center",
        fontsize=13)

# ---- bottom row: finer spacing a_(2), same physical L --------------------
grid(ax, 0.0, 0.4, 2.0, 8)
bracket(ax, 2.25, 0.4, 2.4, r"$L$")
ax.text(1.0, 0.05, r"$(g_0,m_0)_2 \rightarrow a_{(2)}$", ha="center",
        va="top", fontsize=10)

harrow(ax, 3.3, 4.7, 1.4)
ax.text(4.0, 1.72, "same $a_{(2)}$", ha="center", va="bottom", fontsize=8.5)

grid(ax, 5.0, -0.6, 4.0, 16)
bracket(ax, 9.25, -0.6, 3.4, r"$2L$")

harrow(ax, 10.4, 11.2, 1.4)
ax.text(11.5, 1.4, r"$\Sigma(u,\,a_2/L)$", ha="left", va="center",
        fontsize=13)

# ---- same physical L and same u between the rows -------------------------
ax.annotate("", xy=(-0.55, 2.5), xytext=(-0.55, 5.3),
            arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.3,
                            mutation_scale=13))
ax.text(-0.95, 3.9, "same $L$\nsame $\\bar{g}^2(L)$", ha="right",
        va="center", fontsize=10, color=ORANGE)

# ---- continuum extrapolation to sigma(u) ---------------------------------
ax.annotate("", xy=(15.3, 0.9), xytext=(15.3, 6.1),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3,
                            mutation_scale=13))
ax.text(15.6, 3.5, r"$a/L \rightarrow 0$", ha="left", va="center",
        fontsize=9, color=BLUE)
ax.text(15.3, 0.35, r"$\sigma(u)$", ha="center", va="top", fontsize=14)

ax.set_xlim(-3.4, 17.3)
ax.set_ylim(-1.4, 8.8)

fig.savefig("../fig-redraw-048.pdf")
fig.savefig("../fig-redraw-048.png", dpi=200)

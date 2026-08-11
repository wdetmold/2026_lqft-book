"""Redraw of fig-notes-064: the rectangular Wilson loop (contour C) in the
(t, j) plane with corner labels (n,0), (n+rj,0), (n+rj,t), (n,t), directed
edges, and small t/j axes.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_RED = "#D55E00"

T, R = 3.0, 2.0

fig, ax = plt.subplots(figsize=(3.0, 2.1))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, color=C_GREEN, frac=0.5, ms=11):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    m = a + frac * d
    eps = 1e-3 * d
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


# filled rectangle with directed edges (up on left, right on top,
# down on right, left on bottom -- as in the sketch)
ax.add_patch(plt.Rectangle((0, 0), T, R, facecolor=C_GREEN, alpha=0.12,
                           edgecolor="none"))
ax.add_patch(plt.Rectangle((0, 0), T, R, facecolor="none",
                           edgecolor=C_GREEN, lw=2.0, joinstyle="round"))
arrow_on((0, 0), (0, R))          # left edge up
arrow_on((0, R), (T, R))          # top edge right
arrow_on((T, R), (T, 0))          # right edge down
arrow_on((T, 0), (0, 0))          # bottom edge left

# corner labels
fs = 9
ax.text(-0.08, -0.16, r"$(\vec{n},0)$", ha="left", va="top", fontsize=fs)
ax.text(T + 0.08, -0.16, r"$(\vec{n},t)$", ha="right", va="top", fontsize=fs)
ax.text(-0.08, R + 0.14, r"$(\vec{n}+r\hat{\jmath},0)$", ha="left",
        va="bottom", fontsize=fs)
ax.text(T + 0.08, R + 0.14, r"$(\vec{n}+r\hat{\jmath},t)$", ha="right",
        va="bottom", fontsize=fs)

# contour label
ax.text(-0.42, R - 0.35, r"$\mathcal{C}$", color=C_RED, ha="center",
        va="center", fontsize=13)

# small coordinate axes (t horizontal, j vertical)
o = np.array([-1.55, -0.05])
ax.plot([o[0], o[0]], [o[1], o[1] + 0.8], color=C_GREEN, lw=1.4)
ax.plot([o[0], o[0] + 0.8], [o[1], o[1]], color=C_GREEN, lw=1.4)
arrow_on(o, o + np.array([0, 0.8]), frac=1.0, ms=9)
arrow_on(o, o + np.array([0.8, 0]), frac=1.0, ms=9)
ax.text(o[0] - 0.15, o[1] + 0.75, r"$j$", ha="right", va="center", fontsize=10)
ax.text(o[0] + 0.95, o[1] - 0.05, r"$t$", ha="left", va="center", fontsize=10)

ax.set_xlim(-2.0, T + 0.6)
ax.set_ylim(-0.75, R + 0.65)

fig.savefig("../fig-redraw-064.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-064.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 064")

"""Redraw of fig-notes-068: strong-coupling correction 3 -- reverse the
orientation of one tiled plaquette and add N-2 plaquettes of the same
(reversed) orientation, using
int dU U_{a1 b1} ... U_{aN bN} = (1/N!) eps_{a1..aN} eps_{b1..bN} != 0.
SU(3) example: one cell carries two coincident reversed plaquettes
(nested blue squares).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_BLUE = "#0072B2"

T, R = 4, 2

fig, ax = plt.subplots(figsize=(3.0, 2.0))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, color=C_GREEN, frac=0.5, ms=8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    m = a + frac * d
    eps = 1e-3 * d
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def cell(i, j, color=C_GREEN, inset=0.12, orient="left", fill=True):
    x, y, w = i + inset, j + inset, 1 - 2 * inset
    if fill:
        ax.add_patch(plt.Rectangle((x, y), w, w, facecolor=color,
                                   alpha=0.12, edgecolor="none"))
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor="none",
                               edgecolor=color, lw=1.3, joinstyle="round"))
    if orient == "left":
        arrow_on((x + w, y + w), (x, y + w), color=color)
    else:
        arrow_on((x, y + w), (x + w, y + w), color=color)


# tiled 4 x 2 Wilson loop
ax.add_patch(plt.Rectangle((0, 0), T, R, facecolor="none",
                           edgecolor=C_GREEN, lw=1.8, joinstyle="round"))
arrow_on((0, 0), (0, R), ms=10)
arrow_on((0, R), (T, R), ms=10)
arrow_on((T, R), (T, 0), ms=10)
arrow_on((T, 0), (0, 0), ms=10)
for i in range(T):
    for j in range(R):
        if (i, j) != (1, 0):
            cell(i, j)

# the special cell: orientation reversed, N - 2 = 1 extra plaquette with the
# same reversed orientation (two nested blue squares, both "right")
cell(1, 0, color=C_BLUE, inset=0.12, orient="right", fill=True)
cell(1, 0, color=C_BLUE, inset=0.24, orient="right", fill=False)

ax.text(T / 2, -0.45, r"$SU(3)$ example", color=C_BLUE, ha="center",
        va="top", fontsize=10)

ax.set_xlim(-0.35, T + 0.35)
ax.set_ylim(-1.05, R + 0.35)

fig.savefig("../fig-redraw-068.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-068.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 068")

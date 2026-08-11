"""Redraw of fig-notes-016: tiling the rectangular Wilson loop with
plaquettes.  Three panels: (1) the bare R x T loop with lattice-site ticks
(the bare loop vanishes since int dU U_ab = 0); (2) a ring of oppositely
oriented plaquettes along the boundary; (3) the loop fully tiled.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_BLUE = "#0072B2"
C_RED = "#D55E00"

T, R = 5, 3  # loop dimensions in lattice units

fig, ax = plt.subplots(figsize=(6.8, 1.9))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, color=C_GREEN, frac=0.5, ms=10):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    m = a + frac * d
    eps = 1e-3 * d
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def loop(x0, ticks=False):
    """Green R x T Wilson-loop contour at horizontal offset x0."""
    ax.add_patch(plt.Rectangle((x0, 0), T, R, facecolor="none",
                               edgecolor=C_GREEN, lw=1.8, joinstyle="round"))
    arrow_on((x0, 0), (x0, R))              # left up
    arrow_on((x0, R), (x0 + T, R))          # top right
    arrow_on((x0 + T, R), (x0 + T, 0))      # right down
    arrow_on((x0 + T, 0), (x0, 0))          # bottom left
    if ticks:  # lattice sites marked on the contour
        s = 0.09
        for i in range(1, T):
            ax.plot([x0 + i, x0 + i], [-s, s], color=C_GREEN, lw=1.2)
            ax.plot([x0 + i, x0 + i], [R - s, R + s], color=C_GREEN, lw=1.2)
        for j in range(1, R):
            ax.plot([x0 - s, x0 + s], [j, j], color=C_GREEN, lw=1.2)
            ax.plot([x0 + T - s, x0 + T + s], [j, j], color=C_GREEN, lw=1.2)


def plaquette(x0, i, j):
    """Small oppositely oriented (tr P^dagger) plaquette in cell (i, j)."""
    d = 0.16
    x, y = x0 + i + d, j + d
    w = 1 - 2 * d
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor=C_BLUE, alpha=0.12,
                               edgecolor="none"))
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor="none",
                               edgecolor=C_BLUE, lw=1.1, joinstyle="round"))
    arrow_on((x + w, y + w), (x, y + w), color=C_BLUE, ms=7)  # top edge, left


# panel 1: bare loop
X1 = 0.0
loop(X1, ticks=True)
ax.text(X1 - 0.55, R / 2, r"$R$", color=C_BLUE, ha="right", va="center",
        fontsize=11)
ax.text(X1 + T / 2, -0.5, r"$T$", color=C_BLUE, ha="center", va="top",
        fontsize=11)
ax.annotate(r"$\int \mathrm{d}U\, U_{ab} = 0$",
            xy=(X1 + T + 0.06, 1.5), xytext=(X1 + T + 1.15, -0.75),
            color=C_RED, fontsize=9, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=C_RED, lw=1.0,
                            connectionstyle="arc3,rad=0.3"))

# panel 2: ring of plaquettes along the boundary
X2 = 9.4
loop(X2)
for i in range(T):
    for j in range(R):
        if i in (0, T - 1) or j in (0, R - 1):
            plaquette(X2, i, j)

# panel 3: fully tiled loop
X3 = 18.8
loop(X3)
for i in range(T):
    for j in range(R):
        plaquette(X3, i, j)

# arrows between panels
for xa in (X1 + T + 1.6, X2 + T + 1.0):
    arrow_on((xa, R / 2), (xa + 1.6, R / 2), color=C_GREEN, frac=1.0, ms=12)
    ax.plot([xa, xa + 1.55], [R / 2, R / 2], color=C_GREEN, lw=1.4)

ax.set_xlim(X1 - 1.3, X3 + T + 0.4)
ax.set_ylim(-1.15, R + 0.4)

fig.savefig("../fig-redraw-016.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-016.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 016")

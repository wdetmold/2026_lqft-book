"""Redraw of fig-notes-096 (vector note page, CropBox = the second green
example line): the action of the boundary operator on a 2-chain,

    Delta( plaquette ) = (bottom link) + (right link)
                         - (top link) - (left link),

drawn, as in the notes, as an oriented (counter-clockwise) plaquette
mapping to four signed oriented links. Companion of fig-redraw-073
(boundary of a 1-chain), shown in the same figure.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 1.3))
ax.set_aspect("equal")
ax.axis("off")


def link(a, b, ms=11):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=GREEN, lw=1.6,
            solid_capstyle="round", zorder=2)
    m = 0.5 * (a + b)
    eps = 1e-3 * (b - a)
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=GREEN,
                                mutation_scale=ms, shrinkA=0, shrinkB=0),
                zorder=3)


# Delta ( ccw-oriented plaquette ) =
ax.text(-0.15, 0.0, r"$\Delta$", fontsize=14, ha="center", va="center")
ax.text(0.28, -0.04, "(", fontsize=34, ha="center", va="center")
ax.text(1.92, -0.04, ")", fontsize=34, ha="center", va="center")

x0, y0, w = 0.62, -0.48, 0.96
link((x0, y0), (x0 + w, y0))              # bottom ->
link((x0 + w, y0), (x0 + w, y0 + w))      # right ^
link((x0 + w, y0 + w), (x0, y0 + w))      # top <-
link((x0, y0 + w), (x0, y0))              # left v

ax.text(2.38, 0.0, "=", fontsize=13, ha="center", va="center")

# = (bottom ->) (right ^) - (top <-) - (left v)
s = 0.78  # link length
link((2.85, -0.22), (2.85 + s, -0.22))            # ->
link((4.1, -0.39), (4.1, -0.39 + s))              # ^
ax.text(4.55, 0.12, r"$-$", fontsize=13, ha="center", va="center")
link((4.9 + s, 0.22), (4.9, 0.22))                # <-
ax.text(6.05, -0.12, r"$-$", fontsize=13, ha="center", va="center")
link((6.4, 0.39), (6.4, 0.39 - s))                # v

ax.set_xlim(-0.5, 6.85)
ax.set_ylim(-0.85, 0.85)

fig.savefig("../fig-redraw-096.pdf")
fig.savefig("../fig-redraw-096.png", dpi=200)
print("done 096")

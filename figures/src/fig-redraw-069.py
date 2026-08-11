"""Redraw of fig-notes-069: strong-coupling correction 4 -- terms from the
expansion of 1/Z = 1 - O(beta^2): a disconnected vacuum contribution of two
coincident, oppositely oriented plaquettes (U U^dag on the same square),
~ beta^2. Sits inline in an enumerated list, so kept compact.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"

fig, ax = plt.subplots(figsize=(2.1, 1.0))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, color=C_RED, ms=8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = 0.5 * (a + b)
    eps = 1e-3 * (b - a)
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def square(x, y, w, orient, fill=False):
    """Plaquette with orientation arrows on top and bottom edges."""
    if fill:
        ax.add_patch(plt.Rectangle((x, y), w, w, facecolor=C_RED,
                                   alpha=0.12, edgecolor="none"))
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor="none",
                               edgecolor=C_RED, lw=1.4, joinstyle="round"))
    if orient == "cw":       # top edge ->, bottom edge <-
        arrow_on((x, y + w), (x + w, y + w))
        arrow_on((x + w, y), (x, y))
    else:                    # ccw: top edge <-, bottom edge ->
        arrow_on((x + w, y + w), (x, y + w))
        arrow_on((x, y), (x + w, y))


# plaquette and its conjugate on the same square: nested, opposite orientation
square(0.0, 0.0, 1.0, orient="cw")
square(0.14, 0.14, 0.72, orient="ccw", fill=True)

ax.text(1.45, 0.5, r"$\sim \beta^{2}$", fontsize=14, ha="left", va="center")

ax.set_xlim(-0.15, 2.45)
ax.set_ylim(-0.25, 1.25)

fig.savefig("../fig-redraw-069.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-069.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 069")

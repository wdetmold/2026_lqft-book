"""Redraw of fig-notes-067: strong-coupling correction 2 -- add two extra
plaquettes (~beta^2), either on top of an existing tiled plaquette (blue
nested squares with opposite orientation) or elsewhere (standalone nested
pair of oppositely oriented plaquettes), using
int dU U_ab U_cd U^dag_ef U^dag_gh = #(delta delta ...) != 0.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_BLUE = "#0072B2"
C_RED = "#D55E00"

T, R = 4, 2

fig, ax = plt.subplots(figsize=(3.0, 2.3))
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
    """Plaquette square in cell (i, j); orientation arrow on top edge."""
    x, y, w = i + inset, j + inset, 1 - 2 * inset
    ax.add_patch(plt.Rectangle((x, y), w, w,
                               facecolor=color if fill else "none",
                               alpha=0.12 if fill else 1.0,
                               edgecolor="none"))
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor="none",
                               edgecolor=color, lw=1.3, joinstyle="round"))
    if orient == "left":
        arrow_on((x + w, y + w), (x, y + w), color=color)
    else:
        arrow_on((x, y + w), (x + w, y + w), color=color)


# tiled 4 x 2 Wilson loop, all plaquettes same (tr P^dagger) orientation
ax.add_patch(plt.Rectangle((0, 0), T, R, facecolor="none",
                           edgecolor=C_GREEN, lw=1.8, joinstyle="round"))
arrow_on((0, 0), (0, R), ms=10)
arrow_on((0, R), (T, R), ms=10)
arrow_on((T, R), (T, 0), ms=10)
arrow_on((T, 0), (0, 0), ms=10)
for i in range(T):
    for j in range(R):
        cell(i, j)

# two extra plaquettes on an existing tile: nested blue squares with the
# opposite orientation
cell(1, 1, color=C_BLUE, inset=0.20, orient="right", fill=True)
cell(1, 1, color=C_BLUE, inset=0.30, orient="right", fill=False)

# ... or elsewhere: a standalone U U^dag pair (opposite orientations)
x0, y0 = 2.55, -1.55
cell(x0, y0, color=C_RED, inset=0.0, orient="right", fill=True)
cell(x0, y0, color=C_RED, inset=0.13, orient="left", fill=False)

ax.set_xlim(-0.35, T + 0.35)
ax.set_ylim(y0 - 0.35, R + 0.35)

fig.savefig("../fig-redraw-067.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-067.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 067")

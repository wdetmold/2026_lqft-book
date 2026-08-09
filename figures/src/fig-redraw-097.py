"""Redraw of fig-notes-097 (vector-ink crop): example of the action of the
coboundary operator, nabla(.) applied to a point (0-cube) gives the "star"
of the 2d = 8 lattice links containing that site, drawn with the arrows of
the oriented links pointing into the site."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
ORANGE = "#D55E00"

fig, ax = plt.subplots(figsize=(3.0, 1.15))
ax.set_aspect("equal")
ax.axis("off")

# left-hand side: nabla( . ) =
ax.text(-0.95, 0.0, r"$\nabla(\,\cdot\,)\;=$", ha="right", va="center",
        fontsize=15)

# star of the 8 oriented links attached to the site (4 lattice directions,
# two orientations each); arrowheads point into the central site.
R = 0.62          # link length
r_head = 0.10     # arrows stop just outside the site marker
for ang in np.arange(0, 360, 45):
    a = np.deg2rad(ang)
    dx, dy = np.cos(a), np.sin(a)
    ax.annotate("",
                xy=(r_head * dx, r_head * dy),
                xytext=(R * dx, R * dy),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5,
                                mutation_scale=11, shrinkA=0, shrinkB=0))

# the site itself
ax.plot([0], [0], marker="o", ms=6, color=ORANGE, zorder=5)

ax.set_xlim(-2.6, 0.85)
ax.set_ylim(-0.8, 0.8)

fig.savefig("../fig-redraw-097.pdf")
fig.savefig("../fig-redraw-097.png", dpi=200)

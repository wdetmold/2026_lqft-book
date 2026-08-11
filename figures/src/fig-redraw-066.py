"""Redraw of fig-notes-066: strong-coupling correction 1 -- shift one tiled
plaquette out of the plane and add four plaquettes from the action (~beta^4).
A tiled plane of plaquettes in oblique projection with a unit cube (the
shifted plaquette plus four side plaquettes) protruding from one cell.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_BLUE = "#0072B2"

NX, NY = 6, 4  # plane cells


def P(x, y, z=0.0):
    """Oblique projection of lattice point (x, y, z)."""
    return np.array([x + 0.45 * y, 0.48 * y + 0.80 * z])


fig, ax = plt.subplots(figsize=(3.2, 1.7))
ax.set_aspect("equal")
ax.axis("off")

# filled plane
corners = np.array([P(0, 0), P(NX, 0), P(NX, NY), P(0, NY)])
ax.add_patch(plt.Polygon(corners, closed=True, facecolor=C_GREEN,
                         alpha=0.10, edgecolor="none"))
# grid lines
for i in range(NX + 1):
    a, b = P(i, 0), P(i, NY)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GREEN,
            lw=2.0 if i in (0, NX) else 1.0, zorder=2)
for j in range(NY + 1):
    a, b = P(0, j), P(NX, j)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GREEN,
            lw=2.0 if j in (0, NY) else 1.0, zorder=2)

# cube on cell (2,1)-(3,2): the shifted plaquette (top face) + 4 side faces
c = [(2, 1), (3, 1), (3, 2), (2, 2)]
bot = [P(x, y, 0) for (x, y) in c]
top = [P(x, y, 1) for (x, y) in c]


def seg(a, b, hidden=False):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_BLUE, lw=1.9,
            ls=(0, (2.2, 2.2)) if hidden else "-",
            solid_capstyle="round", zorder=4)


# top face (light fill) and vertical edges
ax.add_patch(plt.Polygon(top, closed=True, facecolor=C_BLUE, alpha=0.15,
                         edgecolor="none", zorder=3))
for k in range(4):
    seg(top[k], top[(k + 1) % 4])
for k in range(4):
    seg(bot[k], top[k], hidden=(k == 3))  # rear vertical hidden
# base edges: front two visible, rear two hidden
seg(bot[0], bot[1])
seg(bot[1], bot[2])
seg(bot[2], bot[3], hidden=True)
seg(bot[3], bot[0], hidden=True)

ax.set_xlim(-0.3, P(NX, NY)[0] + 0.3)
ax.set_ylim(-0.25, P(2, 2, 1)[1] + 0.35)

fig.savefig("../fig-redraw-066.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-066.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 066")

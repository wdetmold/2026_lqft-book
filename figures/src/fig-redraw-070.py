"""Redraw of fig-notes-070: depiction of screening in the strong-coupling
expansion. The large Wilson loop (red) is tiled not by a full sheet but by
a tube of fundamental plaquettes along its perimeter (blue slab with a
hole); the zoom balloon shows the individual plaquette cubes lining one
edge of the loop."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle

RED = "#D55E00"
BLUE = "#0072B2"
GREEN = "#009E73"

KX, KY = 0.45, 0.30  # oblique projection of the in-plane depth direction


def P(x, y, z=0.0):
    return (x + KX * y, KY * y + z)


fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

blue = dict(color=BLUE, lw=1.1)
blue_d = dict(color=BLUE, lw=0.9, ls=(0, (2.5, 2.5)))


def line(p, q, **kw):
    ax.plot([p[0], q[0]], [p[1], q[1]], **kw)


def rect(x0, x1, y0, y1, z, **kw):
    pts = [P(x0, y0, z), P(x1, y0, z), P(x1, y1, z),
           P(x0, y1, z), P(x0, y0, z)]
    ax.plot(*zip(*pts), **kw)


# ---- the slab (tube of plaquettes) around the loop perimeter --------------
H = 0.55                                    # slab thickness
ox0, ox1, oy0, oy1 = 0.5, 9.5, 0.4, 5.6     # outer boundary
ix0, ix1, iy0, iy1 = 2.0, 8.0, 1.75, 4.25   # inner hole

rect(ox0, ox1, oy0, oy1, H, **blue)         # top face, outer edge
rect(ix0, ix1, iy0, iy1, H, **blue)         # top face, hole edge

# bottom face: front and right edges visible, back and left hidden
line(P(ox0, oy0, 0), P(ox1, oy0, 0), **blue)
line(P(ox1, oy0, 0), P(ox1, oy1, 0), **blue)
line(P(ox1, oy1, 0), P(ox0, oy1, 0), **blue_d)
line(P(ox0, oy1, 0), P(ox0, oy0, 0), **blue_d)
rect(ix0, ix1, iy0, iy1, 0, **blue_d)       # hidden hole at the bottom

# vertical edges
for (x, y, style) in [(ox0, oy0, blue), (ox1, oy0, blue),
                      (ox1, oy1, blue), (ox0, oy1, blue_d)]:
    line(P(x, y, 0), P(x, y, H), **style)
for (x, y) in [(ix0, iy0), (ix1, iy0)]:
    line(P(x, y, 0), P(x, y, H), **blue_d)

# ---- the large Wilson loop along the middle of the tube -------------------
rect(1.25, 8.75, 1.05, 4.95, H, color=RED, lw=2.6, zorder=5,
     solid_capstyle="round")

# ---- zoom balloon ---------------------------------------------------------
cx, cy, r = 4.9, -3.1, 2.05
src = P(4.6, 0.4, 0.0)  # point on the front edge of the tube

ax.add_patch(Circle((cx, cy), r, fill=False, color=GREEN, lw=1.4, zorder=1))

# tangent lines from src to the balloon
d = np.hypot(cx - src[0], cy - src[1])
th0 = np.arctan2(cy - src[1], cx - src[0])
alpha = np.arcsin(r / d)
for sgn in (+1, -1):
    beta = th0 + sgn * (np.pi / 2 - alpha) + np.pi  # contact angle from center
    tp = (cx + r * np.cos(th0 + sgn * (np.pi / 2 + alpha - np.pi)),
          cy + r * np.sin(th0 + sgn * (np.pi / 2 + alpha - np.pi)))
    # contact point: rotate by +/- (pi/2 - alpha) about the center
    tp = (cx - r * np.cos(th0 - sgn * (np.pi / 2 - alpha)),
          cy - r * np.sin(th0 - sgn * (np.pi / 2 - alpha)))
    line(src, tp, color=GREEN, lw=1.2)

# zoomed content: the loop edge with a row of plaquette cubes below it
ax.plot([3.25, 6.55], [-2.30, -2.30], color=RED, lw=2.8,
        solid_capstyle="round", zorder=5)


def qp(x, y, z):  # local oblique projection for the little cubes
    return (x + 0.35 * y, 0.22 * y + z)


def cube(x0, z0, w, dep, h):
    A_, B_ = qp(x0, 0, z0), qp(x0 + w, 0, z0)
    C_, D_ = qp(x0 + w, 0, z0 + h), qp(x0, 0, z0 + h)
    Ab, Bb = qp(x0, dep, z0), qp(x0 + w, dep, z0)
    Cb, Db = qp(x0 + w, dep, z0 + h), qp(x0, dep, z0 + h)
    for p_, q_ in [(A_, B_), (B_, C_), (C_, D_), (D_, A_),  # front face
                   (D_, Db), (C_, Cb), (Db, Cb),            # top face
                   (B_, Bb)]:                               # right face
        line(p_, q_, **blue)
    for p_, q_ in [(A_, Ab), (Ab, Bb), (Ab, Db)]:           # hidden edges
        line(p_, q_, **blue_d)


ncube, w = 5, 0.62
for i in range(ncube):
    cube(3.35 + i * w, -3.45, w, 0.5, 0.5)

ax.set_xlim(-0.4, 12.4)
ax.set_ylim(-5.5, 2.6)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-070.pdf")
fig.savefig("../fig-redraw-070.png", dpi=200)
print("done 070")

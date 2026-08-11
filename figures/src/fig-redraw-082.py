"""Redraw of fig-notes-082: quark-line diagram for the pion two-point
function.  Two quark propagators (arcs with opposite direction arrows)
between the sink at x = (vec x, t) and the source at y = (vec y, 0).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
INK = "0.15"


def bezier(p0, p1, p2, p3, n=200):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def draw_curve(ax, pts, color=BLUE, lw=1.6, arrow=0):
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw,
            solid_capstyle="round", zorder=2)
    if arrow:
        i = len(pts) // 2
        d = 4 if arrow > 0 else -4
        ax.annotate("", xy=pts[i + d], xytext=pts[i - d],
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    shrinkA=0, shrinkB=0,
                                    mutation_scale=14), zorder=3)


fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

xL = np.array([-1.5, 0.0])   # sink,  x = (vec x, t)
xR = np.array([1.5, 0.0])    # source, y = (vec y, 0)

# Upper propagator: arrow pointing to the right (as in the sketch).
up = bezier(xL, (-0.8, 0.85), (0.8, 0.85), xR)
draw_curve(ax, up, arrow=+1)

# Lower propagator: arrow pointing to the left.
dn = bezier(xL, (-0.8, -0.85), (0.8, -0.85), xR)
draw_curve(ax, dn, arrow=-1)

for p in (xL, xR):
    ax.plot(*p, marker="o", ms=7, color=INK, zorder=4)

ax.text(xL[0] - 0.18, xL[1] - 0.32, r"$x$", ha="right", va="top",
        fontsize=13, color=INK)
ax.text(xR[0] + 0.18, xR[1] - 0.32, r"$y$", ha="left", va="top",
        fontsize=13, color=INK)

ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-1.35, 1.25)

fig.savefig("../fig-redraw-082.pdf")
fig.savefig("../fig-redraw-082.png", dpi=200)
print("done")

"""Redraw of fig-notes-084: contributions to the correlation function for
a flavour-singlet set of states.  Left: quark-line connected diagram
(two propagators between Gamma and Gamma').  Right: quark-line
disconnected diagram (a closed quark loop at Gamma and another at
Gamma').
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


def draw_curve(ax, pts, arrow=0):
    ax.plot(pts[:, 0], pts[:, 1], color=BLUE, lw=1.5,
            solid_capstyle="round", zorder=2)
    if arrow:
        i = len(pts) // 2
        d = 4 if arrow > 0 else -4
        ax.annotate("", xy=pts[i + d], xytext=pts[i - d],
                    arrowprops=dict(arrowstyle="-|>", color=BLUE,
                                    shrinkA=0, shrinkB=0,
                                    mutation_scale=13), zorder=3)


fig, ax = plt.subplots(figsize=(6.4, 2.1))
ax.set_aspect("equal")
ax.axis("off")

# ---- connected diagram -------------------------------------------------
cL = np.array([-4.1, 0.0])
cR = np.array([-1.5, 0.0])
draw_curve(ax, bezier(cL, (-3.5, 0.75), (-2.1, 0.75), cR), arrow=+1)
draw_curve(ax, bezier(cL, (-3.5, -0.75), (-2.1, -0.75), cR), arrow=-1)
for p in (cL, cR):
    ax.plot(*p, marker="o", ms=6, color=INK, zorder=4)
ax.text(cL[0] - 0.22, cL[1] + 0.12, r"$\Gamma$", ha="right", va="bottom",
        fontsize=13, color=INK)
ax.text(cR[0] + 0.22, cR[1] + 0.12, r"$\Gamma'$", ha="left", va="bottom",
        fontsize=13, color=INK)

# ---- disconnected diagram ----------------------------------------------
r = 0.62
for xc, dot_side, lab, lab_side in [(1.6, -1, r"$\Gamma$", -1),
                                    (3.6, +1, r"$\Gamma'$", +1)]:
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(xc + r * np.cos(th), r * np.sin(th), color=BLUE, lw=1.5,
            zorder=2)
    xd = xc + dot_side * r
    ax.plot(xd, 0.0, marker="o", ms=6, color=INK, zorder=4)
    ax.text(xd + lab_side * 0.24, 0.12, lab,
            ha=("right" if lab_side < 0 else "left"), va="bottom",
            fontsize=13, color=INK)

ax.text(2.6, -1.05, '"quark-line disconnected"', ha="center", va="top",
        fontsize=10, color=INK)

ax.set_xlim(-4.9, 4.9)
ax.set_ylim(-1.55, 1.05)

fig.savefig("../fig-redraw-084.pdf")
fig.savefig("../fig-redraw-084.png", dpi=200)
print("done")

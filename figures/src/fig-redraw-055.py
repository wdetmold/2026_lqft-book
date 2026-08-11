"""Redraw of fig-notes-055: non-vanishing potential contributions to Z_4 in
the hopping expansion. Left to right: two disjoint doubled links; two doubled
links sharing a site; a plaquette (four-link loop); a quadrupled link. Below
each graph: the gamma content, the counting of placements, and the
combinatoric factor from the expansion of the exponential.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import FancyArrowPatch, Rectangle

C_FRAME = "#0072B2"
C_GRAPH = "#D55E00"

fig, axes = plt.subplots(1, 4, figsize=(9.8, 3.3))

DOT = dict(marker="o", ms=5.5, color=C_GRAPH, ls="none", zorder=4)


def frame(ax):
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor=C_FRAME,
                           lw=1.6, zorder=1))
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.95, 1.02)


def link(ax, a, b):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GRAPH, lw=1.6,
            solid_capstyle="round", zorder=3)
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


def multi_link(ax, a, b, rads):
    for r in rads:
        if r == 0:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GRAPH, lw=1.6,
                    solid_capstyle="round", zorder=3)
        else:
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-",
                                         connectionstyle=f"arc3,rad={r}",
                                         color=C_GRAPH, lw=1.6, zorder=3))
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


def labels(ax, gam, count, fact):
    ax.text(0.5, -0.20, gam, ha="center", va="center", fontsize=11)
    ax.text(0.5, -0.48, count, ha="center", va="center", fontsize=9)
    ax.text(0.5, -0.78, fact, ha="center", va="center", fontsize=10)


# row headers to the left of the first panel
axes[0].text(-0.14, -0.48, "counting:", ha="right", va="center",
             fontsize=9, color="0.35", clip_on=False)
axes[0].text(-0.14, -0.78, "comb. factor:", ha="right", va="center",
             fontsize=9, color="0.35", clip_on=False)

# ---- 1: two disjoint doubled links ~ gamma_2^4 ----------------------------
ax = axes[0]
frame(ax)
multi_link(ax, (0.52, 0.74), (0.78, 0.74), [-0.5, 0.5])
multi_link(ax, (0.26, 0.22), (0.26, 0.48), [-0.5, 0.5])
labels(ax, r"$\sim\gamma_2^4$",
       r"$4\Omega\,(4\Omega-7\cdot2-1)/2$",
       r"$\frac{1}{2!\,2!}$")

# ---- 2: two doubled links sharing a site ~ gamma_2^2 gamma_4 --------------
ax = axes[1]
frame(ax)
multi_link(ax, (0.38, 0.60), (0.66, 0.60), [-0.5, 0.5])
multi_link(ax, (0.38, 0.32), (0.38, 0.60), [-0.5, 0.5])
labels(ax, r"$\sim\gamma_2^2\gamma_4$",
       r"$4\Omega\cdot7\cdot 2/2$",
       r"$\frac{1}{2!\,2!}$")

# ---- 3: plaquette ~ gamma_2^4 ---------------------------------------------
ax = axes[2]
frame(ax)
p = [(0.38, 0.34), (0.66, 0.34), (0.66, 0.62), (0.38, 0.62)]
for i in range(4):
    link(ax, p[i], p[(i + 1) % 4])
labels(ax, r"$\sim\gamma_2^4$",
       r"$\Omega\cdot 4\cdot3/2$",
       r"$1$")

# ---- 4: quadrupled link ~ gamma_4^2 ---------------------------------------
ax = axes[3]
frame(ax)
multi_link(ax, (0.34, 0.52), (0.68, 0.52), [-0.55, -0.2, 0.2, 0.55])
labels(ax, r"$\sim\gamma_4^2$",
       r"$4\Omega$",
       r"$\frac{1}{4!}$")

fig.savefig("../fig-redraw-055.pdf")
fig.savefig("../fig-redraw-055.png", dpi=200)

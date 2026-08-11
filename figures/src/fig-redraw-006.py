"""Redraw of fig-notes-006: potential contributions to Z_2 in the hopping
expansion (A, B, C from left to right).

A: two disjoint links <l,m> and <p,q> (open circles mark sites p cannot
   occupy for the links to be disjoint);
B: two links sharing one site (p = l);
C: the same link taken twice (p = l, q = m).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import FancyArrowPatch, Rectangle

C_FRAME = "#0072B2"   # lattice region
C_GRAPH = "#D55E00"   # hopping links / sites
C_ANN = "#009E73"     # annotation

fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9))

DOT = dict(marker="o", ms=6, color=C_GRAPH, ls="none", zorder=4)


def frame(ax):
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor=C_FRAME,
                           lw=1.6, zorder=1))
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)


def link(ax, a, b):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GRAPH, lw=1.6,
            solid_capstyle="round", zorder=3)
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


def double_link(ax, a, b, rad=0.45):
    for r in (rad, -rad):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-",
                                     connectionstyle=f"arc3,rad={r}",
                                     color=C_GRAPH, lw=1.6, zorder=3))
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


# ---- A: disjoint links <l,m> and <p,q> ------------------------------------
ax = axes[0]
frame(ax)
l, m = (0.28, 0.76), (0.46, 0.76)
link(ax, l, m)
ax.text(l[0] - 0.02, l[1] + 0.06, "$l$", ha="center", va="bottom",
        color=C_GRAPH, fontsize=10)
ax.text(m[0] + 0.02, m[1] + 0.06, "$m$", ha="center", va="bottom",
        color=C_GRAPH, fontsize=10)
# excluded sites for p (open circles)
excl = [(0.10, 0.76), (0.28, 0.58), (0.46, 0.58)]
for e in excl:
    ax.plot(*e, marker="o", ms=6, mfc="none", mec=C_ANN, mew=1.3,
            ls="none", zorder=4)
ax.annotate("$p$ can't\nbe here", xy=(0.50, 0.575), xytext=(0.68, 0.60),
            color=C_ANN, fontsize=9, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C_ANN, lw=0.9,
                            shrinkA=2, shrinkB=3))
q, p = (0.24, 0.36), (0.24, 0.18)
link(ax, q, p)
ax.text(q[0] - 0.06, q[1], "$q$", ha="right", va="center",
        color=C_GRAPH, fontsize=10)
ax.text(p[0] - 0.06, p[1], "$p$", ha="right", va="center",
        color=C_GRAPH, fontsize=10)

# ---- B: two links sharing one site (p = l) --------------------------------
ax = axes[1]
frame(ax)
c, u, r = (0.44, 0.42), (0.44, 0.62), (0.64, 0.42)
link(ax, c, u)
link(ax, c, r)
ax.text(u[0], u[1] + 0.06, "$q$", ha="center", va="bottom",
        color=C_GRAPH, fontsize=10)
ax.text(c[0] - 0.05, c[1] - 0.08, "$p=l$", ha="right", va="center",
        color=C_GRAPH, fontsize=10)
ax.text(r[0] + 0.02, r[1] - 0.09, "$m$", ha="center", va="top",
        color=C_GRAPH, fontsize=10)

# ---- C: doubled link (p = l, q = m) ---------------------------------------
ax = axes[2]
frame(ax)
a, b = (0.36, 0.52), (0.62, 0.52)
double_link(ax, a, b)
ax.text(a[0] - 0.05, a[1], "$p=l$", ha="right", va="center",
        color=C_GRAPH, fontsize=10)
ax.text(b[0] + 0.05, b[1], "$q=m$", ha="left", va="center",
        color=C_GRAPH, fontsize=10)

fig.savefig("../fig-redraw-006.pdf")
fig.savefig("../fig-redraw-006.png", dpi=200)

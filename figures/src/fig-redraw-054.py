"""Redraw of fig-notes-054: potential contributions to Z_3 in the hopping
expansion (all vanish, since each involves gamma_j with odd j).

Left to right: tripled link; doubled link + disjoint link; doubled link with
an extra link at one end; three disjoint links; three-link path; two-link
corner + disjoint link; three links meeting at one site; ...
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import FancyArrowPatch

C = "#D55E00"

fig, ax = plt.subplots(figsize=(9.6, 1.7))
ax.set_aspect("equal")
ax.set_axis_off()

DOT = dict(marker="o", ms=5.5, color=C, ls="none", zorder=4)


def link(a, b):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C, lw=1.6,
            solid_capstyle="round", zorder=3)
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


def multi_link(a, b, rads):
    for r in rads:
        if r == 0:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=C, lw=1.6,
                    solid_capstyle="round", zorder=3)
        else:
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-",
                                         connectionstyle=f"arc3,rad={r}",
                                         color=C, lw=1.6, zorder=3))
    ax.plot([a[0], b[0]], [a[1], b[1]], **DOT)


u = 0.55       # link length
x = 0.0        # running x origin
GAP = 0.62     # gap containing the comma


def comma(x):
    ax.text(x, -0.62, ",", color="k", fontsize=13, ha="center",
            va="center")


# 1: tripled link  ~ gamma_3^2
multi_link((x, 0), (x + u, 0), [-0.5, 0.0, 0.5])
x += u + GAP
comma(x - GAP / 2)

# 2: doubled link + disjoint single link  ~ gamma_2^2 gamma_1^2
multi_link((x, 0.28), (x + u, 0.28), [-0.5, 0.5])
link((x + 0.06, -0.18), (x + 0.06, -0.62))
x += u + GAP
comma(x - GAP / 2)

# 3: doubled link with an extra link at one end  ~ gamma_3 gamma_2 gamma_1
multi_link((x, -0.15), (x + u, -0.15), [-0.5, 0.5])
link((x, -0.15), (x, -0.15 + u))
x += u + GAP
comma(x - GAP / 2)

# 4: three disjoint links  ~ gamma_1^6
link((x, 0.45), (x + 0.5, 0.45))
link((x + 0.35, 0.02), (x + 0.85, 0.02))
link((x + 0.05, -0.18), (x + 0.05, -0.62))
x += 0.85 + GAP
comma(x - GAP / 2)

# 5: three-link path  ~ gamma_1^2 gamma_2^2
link((x, -0.55), (x, 0))
link((x, 0), (x + 0.5, 0))
link((x + 0.5, 0), (x + 0.5, 0.55))
x += 0.5 + GAP
comma(x - GAP / 2)

# 6: two-link corner + disjoint link  ~ gamma_2 gamma_1^4
link((x, 0.35), (x + 0.5, 0.35))
link((x, 0.35), (x, -0.2))
link((x + 0.85, 0.12), (x + 0.85, -0.32))
x += 0.85 + GAP
comma(x - GAP / 2)

# 7: three links meeting at one site  ~ gamma_3 gamma_1^3
link((x, 0), (x, 0.5))
link((x, 0), (x, -0.55))
link((x, 0), (x + 0.5, 0))
x += 0.5 + GAP
comma(x - GAP / 2)

ax.text(x + 0.05, -0.05, r"$\cdots$", color="k", fontsize=13,
        ha="left", va="center")

ax.set_xlim(-0.25, x + 0.7)
ax.set_ylim(-0.85, 0.75)

fig.savefig("../fig-redraw-054.pdf")
fig.savefig("../fig-redraw-054.png", dpi=200)

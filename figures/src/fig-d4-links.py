"""D_4 for lattice gauge theory, figure 1: link variables and elementary loops,
drawn in dimensions one can see.

(a) a site of D_3 = fcc with its 12 link variables U_e(x)
(b) the minimal Wilson loop on D_3: a TRIANGLE of three links
(c) the cubic lattice for contrast: 6 links, bipartite, minimal loop is a square
(d) loop inventory per site, D_4 against Z^4

Counts (all verified by enumeration):
  D_4   12 independent link directions; 96 triangles through a site (32/site);
        936 four-link loops through a site, of which 264 planar rhombi
  Z^4    4 independent link directions;  0 triangles; 24 squares through a site
  D_3   12 neighbours, 24 triangles through a site
  Z^3    6 neighbours,  0 triangles, 12 squares through a site
"""
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

plt.style.use("lqftbook.mplstyle")

C_SITE = "#0072B2"
C_LINK = "#7FA9C9"
C_LOOP = "#D55E00"
C_ALT = "#009E73"
C_TXT = "#444444"

FCC = np.array([v for v in itertools.product((-1, 0, 1), repeat=3)
                if sum(x * x for x in v) == 2], float)
CUB = np.array([v for v in itertools.product((-1, 0, 1), repeat=3)
                if sum(abs(x) for x in v) == 1], float)

fig = plt.figure(figsize=(7.5, 5.9))
gs = fig.add_gridspec(2, 2, hspace=0.22, wspace=0.20)


def arrow3(ax, a, b, color, lw=1.1, head=0.20, zorder=4):
    """A line with a small cone-free arrowhead (a short thick segment at 80%)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ax.plot(*zip(a, b), color=color, lw=lw, zorder=zorder, solid_capstyle="round")
    m = a + (1 - head) * (b - a)
    ax.plot(*zip(m, b), color=color, lw=lw * 2.6, zorder=zorder,
            solid_capstyle="butt")


# ------------------------------------------------------------ (a) 12 links
ax = fig.add_subplot(gs[0, 0], projection="3d")
for e in FCC:
    arrow3(ax, np.zeros(3), e, C_LINK)
ax.scatter(*FCC.T, s=22, color=C_SITE, depthshade=False, zorder=5)
ax.scatter([0], [0], [0], s=55, color=C_LOOP, depthshade=False, zorder=6)
ax.text(0.16, 0.06, 0.34, r"$x$", fontsize=10, color=C_LOOP)
ax.text(0.72, 0.72, 0.30, r"$U_e(x)$", fontsize=9.5, color="#5588AA")
ax.set_title(r"(a) link variables on $D_3=$ fcc: $12$ per site", fontsize=9.5)
ax.text2D(0.5, 0.075, r"in $d=4$: $24$ links, $12$ independent directions",
          transform=ax.transAxes, ha="center", fontsize=8.5, color=C_TXT)
ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(elev=20, azim=-58)
for L in (ax.set_xlim, ax.set_ylim, ax.set_zlim): L(-1.08, 1.08)

# ------------------------------------------------ (b) triangular plaquette
ax = fig.add_subplot(gs[0, 1], projection="3d")
for e in FCC:
    arrow3(ax, np.zeros(3), e, "#DDE7EE", lw=0.8, zorder=2)
ax.scatter(*FCC.T, s=14, color="#BBD0DE", depthshade=False, zorder=3)
tri = np.array([[0, 0, 0], [1, 1, 0], [1, 0, 1]], float)
ax.add_collection3d(Poly3DCollection([tri], facecolor=C_LOOP, alpha=0.16,
                                     edgecolor="none"))
for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
    arrow3(ax, a, b, C_LOOP, lw=1.7, zorder=7)
ax.scatter(*tri.T, s=34, color=C_LOOP, depthshade=False, zorder=8)
ax.set_title(r"(b) the minimal loop is a triangle", fontsize=9.5)
ax.text2D(0.5, 0.075,
          r"$\mathrm{Tr}\,U_{\triangle}= \mathrm{Tr}\,[\,U_{e_1}U_{e_2}U_{e_3}]$"
          "\n" r"$96$ triangles through each site of $D_4$",
          transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=C_TXT)
ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(elev=20, azim=-58)
for L in (ax.set_xlim, ax.set_ylim, ax.set_zlim): L(-1.08, 1.08)

# -------------------------------------------------------- (c) cubic contrast
ax = fig.add_subplot(gs[1, 0], projection="3d")
for e in CUB:
    arrow3(ax, np.zeros(3), e, "#DDE7EE", lw=0.9, zorder=2)
ax.scatter(*CUB.T, s=16, color="#BBD0DE", depthshade=False, zorder=3)
sq = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], float)
ax.add_collection3d(Poly3DCollection([sq], facecolor=C_ALT, alpha=0.15,
                                     edgecolor="none"))
for i in range(4):
    arrow3(ax, sq[i], sq[(i + 1) % 4], C_ALT, lw=1.7, zorder=7)
ax.scatter(*sq.T, s=30, color=C_ALT, depthshade=False, zorder=8)
ax.set_title(r"(c) hypercubic: bipartite, so no triangles", fontsize=9.5)
ax.text2D(0.5, 0.075,
          r"the minimal loop is the $4$-link plaquette" "\n"
          r"$\mathrm{Tr}\,U_{\mathrm{P}}$, $24$ through each site of $\mathbb{Z}^4$",
          transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=C_TXT)
ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(elev=20, azim=-58)
ax.set_xlim(-1.1, 1.25); ax.set_ylim(-1.1, 1.25); ax.set_zlim(-1.15, 1.15)

# --------------------------------------------------------- (d) loop counts
ax = fig.add_subplot(gs[1, 1])
labels = ["links\n(directions)", "3-link\nloops", "4-link\nloops",
          "planar\nrhombi"]
d4 = [12, 96, 936, 264]
z4 = [4, 0, 24, 24]
xs = np.arange(len(labels)); w = 0.36
ax.bar(xs - w / 2, d4, w, color=C_SITE, label=r"$D_4$")
ax.bar(xs + w / 2, z4, w, color=C_ALT, label=r"$\mathbb{Z}^4$")
ax.set_yscale("log")
for x, (a, b) in enumerate(zip(d4, z4)):
    ax.text(x - w / 2, a * 1.25, str(a), ha="center", fontsize=8, color=C_SITE)
    ax.text(x + w / 2, max(b, 0.55) * 1.25, str(b), ha="center", fontsize=8,
            color=C_ALT)
ax.set_xticks(xs); ax.set_xticklabels(labels, fontsize=8)
ax.set_ylabel("count per site")
ax.set_ylim(0.5, 4000)
ax.text(-0.35, 2100, r"$D_4$", color=C_SITE, fontsize=10, ha="left")
ax.text(0.35, 2100, r"$\mathbb{Z}^4$", color=C_ALT, fontsize=10, ha="left")
ax.set_title(r"(d) loops through a site", fontsize=9.5)

fig.savefig("../fig-d4-links.pdf")
fig.savefig("../fig-d4-links.png", dpi=200)
print("wrote fig-d4-links")

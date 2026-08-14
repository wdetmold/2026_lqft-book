"""D_4 conventions, figure 1: the two constructions, and how the dual behaves
with dimension.

(a) checkerboard construction  D_d = {x in Z^d : sum x_mu even}, drawn in d=2
(b) body-centred construction  D_d* = Z^d u (Z^d + (1/2,...,1/2)), drawn in d=2
(c) d=3, where the two are genuinely different lattices: fcc vs bcc
(d) kissing numbers vs d: the dual's minimal vectors switch from the 2^d body
    diagonals to the 2d axial vectors, and only at d=4 do both occur at once
    and match D_d.  (d=2 also matches, but there D_2 is just a rescaled Z^2.)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

plt.style.use("lqftbook.mplstyle")

C_LAT = "#0072B2"   # lattice points
C_OFF = "#BBBBBB"   # points of Z^d not in the lattice
C_GLU = "#D55E00"   # glue / centre points
C_DUA = "#009E73"   # dual lattice
C_MRK = "#CC79A7"

fig = plt.figure(figsize=(7.4, 6.2))
gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.26)

# --------------------------------------------------------------- (a) D_2
ax = fig.add_subplot(gs[0, 0])
R = 3
for i in range(-R, R + 1):
    for j in range(-R, R + 1):
        if (i + j) % 2 == 0:
            ax.plot(i, j, "o", ms=6, color=C_LAT, zorder=3)
        else:
            ax.plot(i, j, "o", ms=4, mfc="white", mec=C_OFF, mew=1.0, zorder=2)
for e in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
    ax.annotate("", xy=e, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=C_MRK, lw=1.4,
                                shrinkA=0, shrinkB=3))
ax.plot(0, 0, "o", ms=7, color=C_MRK, zorder=4)
ax.set_title(r"(a) checkerboard: $D_d=\{x\in\mathbb{Z}^d:\sum_\mu x_\mu\ \mathrm{even}\}$",
             fontsize=9.5)
ax.text(0, -R - 1.0, "keep the filled sites\n" + r"$2d(d\!-\!1)$ neighbours at $|e|^2=2$",
        ha="center", va="top", fontsize=8.5, color="#444444")
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-R - .6, R + .6); ax.set_ylim(-R - 2.4, R + .6)

# --------------------------------------------------------------- (b) D_2*
ax = fig.add_subplot(gs[0, 1])
for i in range(-R, R + 1):
    for j in range(-R, R + 1):
        ax.plot(i, j, "o", ms=6, color=C_LAT, zorder=3)
for i in range(-R, R):
    for j in range(-R, R):
        ax.plot(i + .5, j + .5, "s", ms=5.5, color=C_GLU, zorder=3)
for e in [(.5, .5), (.5, -.5), (-.5, .5), (-.5, -.5)]:
    ax.annotate("", xy=e, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=C_MRK, lw=1.8,
                                mutation_scale=13, shrinkA=0, shrinkB=5))
    ax.plot(*e, "s", ms=8, mfc="none", mec=C_MRK, mew=1.6, zorder=5)
ax.plot(0, 0, "o", ms=7, color=C_MRK, zorder=4)
ax.set_title(r"(b) body-centred: $D_d^{*}=\mathbb{Z}^d\cup(\mathbb{Z}^d+(\frac{1}{2},\dots,\frac{1}{2}))$",
             fontsize=9.5)
ax.text(0, -R - 1.0, "integer sites plus cell centres\n" + r"$2^d$ diagonals at $|e|^2=d/4$",
        ha="center", va="top", fontsize=8.5, color="#444444")
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-R - .6, R + .6); ax.set_ylim(-R - 2.4, R + .6)

# --------------------------------------------------------------- (c) d=3
ax = fig.add_subplot(gs[1, 0], projection="3d")
cube = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)], float)
edges = [(a, b) for a in range(8) for b in range(a + 1, 8)
         if np.abs(cube[a] - cube[b]).sum() == 1]
FACES = [[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]]
def draw_cube(off):
    polys = [[cube[i] + off for i in f] for f in FACES]
    ax.add_collection3d(Poly3DCollection(polys, facecolor="#5B8FB9", alpha=0.07,
                                         edgecolor="none", zsort="min"))
    segs = [[cube[a] + off, cube[b] + off] for a, b in edges]
    ax.add_collection3d(Line3DCollection(segs, colors="#B0B0B0", lw=0.9))
    ax.scatter(*(cube + off).T, s=17, color=C_LAT, depthshade=False, zorder=6)
draw_cube(np.zeros(3))
faces = np.array([[.5, .5, 0], [.5, .5, 1], [.5, 0, .5],
                  [.5, 1, .5], [0, .5, .5], [1, .5, .5]])
ax.scatter(*faces.T, s=30, color=C_GLU, depthshade=False, marker="s",
           edgecolor="white", linewidth=0.6, zorder=8)
off = np.array([2.3, 0, 0])
draw_cube(off)
ax.scatter(*(np.array([[.5, .5, .5]]) + off).T, s=34, color=C_GLU,
           depthshade=False, marker="s", edgecolor="white", linewidth=0.6, zorder=8)
ax.text(0.5, 0.5, -1.15, r"$D_3$ = fcc,  $\tau=12$", ha="center", fontsize=9, color="#333333")
ax.text(2.8, 0.5, -1.15, r"$D_3^{*}$ = bcc,  $\tau=8$", ha="center", fontsize=9, color="#333333")
ax.set_title(r"(c) $d=3$: the dual is a different lattice", fontsize=9.5)
ax.set_box_aspect((3.0, 1.0, 1.15)); ax.axis("off")
ax.view_init(elev=20, azim=-62)
ax.set_xlim(-.2, 3.5); ax.set_ylim(-.2, 1.2); ax.set_zlim(-1.0, 1.2)

# --------------------------------------------------------------- (d) kissing
ax = fig.add_subplot(gs[1, 1])
ds = np.arange(2, 9)
kd = 2 * ds * (ds - 1)
kds = np.array([2**d if d < 4 else (2**d + 2 * d if d == 4 else 2 * d) for d in ds])
ax.semilogy(ds, kd, "o-", color=C_LAT, lw=1.8, ms=5)
ax.semilogy(ds, kds, "s--", color=C_DUA, lw=1.8, ms=5)
ax.plot([4], [24], "o", ms=13, mfc="none", mec=C_MRK, mew=2.0, zorder=5)
ax.annotate("both $=24$", xy=(4, 24), xytext=(2.05, 46),
            fontsize=9, color=C_MRK, ha="left",
            arrowprops=dict(arrowstyle="-", color=C_MRK, lw=1.0,
                            shrinkA=2, shrinkB=8))
ax.text(8.15, 130, r"$D_d$", color=C_LAT, fontsize=10, ha="right")
ax.text(8.15, 21.5, r"$D_d^{*}$", color=C_DUA, fontsize=10, ha="right")
ax.text(2.1, 4.2, "dual min:\n$2^d$ diagonals", fontsize=7.6, color="#555555", va="top")
ax.text(5.1, 4.2, "dual min:\n$2d$ axial", fontsize=7.6, color="#555555", va="top")
ax.axvline(4, color="#DDDDDD", lw=0.8, zorder=0)
ax.set_xlabel(r"$d$"); ax.set_ylabel("kissing number")
ax.set_title(r"(d) how the dual behaves with dimension", fontsize=9.5)
ax.set_xlim(1.7, 8.3); ax.set_ylim(2.4, 420)

fig.savefig("../fig-d4-constructions.pdf")
fig.savefig("../fig-d4-constructions.png", dpi=200)
print("wrote fig-d4-constructions")

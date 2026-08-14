"""D_4 for lattice gauge theory, figure 2: the neighbour polytope read as the
plaquette structure of the gauge theory.

The centre of each panel is a site x. The radial lines are its link variables;
the outer points are its neighbours. A chord between two neighbours e, f exists
exactly when e-f is itself a lattice vector -- i.e. exactly when x, x+e, x+f
close a TRIANGULAR plaquette. So on D_4 the 96 edges of the 24-cell ARE the 96
elementary triangles through the site, while on Z^4 the same construction gives
no chords at all: the hypercubic lattice is bipartite and its minimal Wilson
loop needs four links.

(a) root convention, one triangle highlighted
(b) body-centred convention: the same picture, links coloured by type
(c) hypercubic: 8 links, no chords
"""
import itertools
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_LINK = "#9DBEDC"
C_SITE = "#0072B2"
C_LOOP = "#D55E00"
C_AX = "#D55E00"
C_DI = "#009E73"
C_HC = "#009E73"
C_TXT = "#444444"

S1 = np.array([v for v in itertools.product(range(-2, 3), repeat=4)
               if sum(v) % 2 == 0 and sum(x * x for x in v) == 2], float)
BCH = np.array([np.array(v, float) for v in itertools.product((-1, 0, 1), repeat=4)
                if sum(x * x for x in v) == 1] +
               [np.array(s, float) * .5 for s in itertools.product((-1, 1), repeat=4)])
is_axial = np.array([np.isclose(np.abs(v).max(), 1.0) for v in BCH])
R = np.array([[1, 1, 0, 0], [1, -1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]]) / np.sqrt(2)
BCH_M = np.sqrt(2) * BCH @ R.T
HC = np.array([v for v in itertools.product((-1, 0, 1), repeat=4)
               if sum(abs(x) for x in v) == 1], float)


def coxeter_plane(simple, order):
    M = np.eye(4)
    for r in simple:
        r = r / np.linalg.norm(r)
        M = (np.eye(4) - 2 * np.outer(r, r)) @ M
    w, V = np.linalg.eig(M)
    k = np.argmin(np.abs(np.angle(w) - 2 * np.pi / order))
    z = V[:, k]
    u, v = np.real(z), np.imag(z)
    u /= np.linalg.norm(u); v -= (v @ u) * u; v /= np.linalg.norm(v)
    return np.vstack([u, v])

P_F4 = coxeter_plane(np.array([[0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1],
                               [.5, -.5, -.5, -.5]]), 12)
P_B4 = coxeter_plane(np.array([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, -1],
                               [0, 0, 0, 1]]), 8)

fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.5))


def panel(ax, pts, P, ip_edge, vcols, chord_col=C_LINK, ms=5.6, link_col=C_LINK):
    xy = pts @ P.T
    for i in range(len(pts)):                       # the links U_e(x)
        ax.plot([0, xy[i, 0]], [0, xy[i, 1]], color=link_col, lw=0.65, zorder=1)
    n_ch = 0
    if ip_edge is not None:                         # chords = closing links
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if np.isclose(pts[i] @ pts[j], ip_edge):
                    ax.plot(*zip(xy[i], xy[j]), color=chord_col, lw=0.6, zorder=1)
                    n_ch += 1
    for i in range(len(pts)):
        ax.plot(*xy[i], "o", ms=ms,
                color=vcols[i] if isinstance(vcols, list) else vcols,
                mec="white", mew=0.7, zorder=4)
    ax.plot(0, 0, "o", ms=6.5, color="#333333", zorder=6)
    return xy, n_ch


# ------------------------------------------------------------------ (a)
ax = axes[0]
xy, n = panel(ax, S1, P_F4, 1.0, C_SITE)
# pick the adjacent pair whose projected vertices are most widely separated,
# so the highlighted triangle reads clearly
cand = [(a, b) for a in range(len(S1)) for b in range(len(S1))
        if a < b and np.isclose(S1[a] @ S1[b], 1.0)]
i, j = max(cand, key=lambda ab: np.linalg.norm(xy[ab[0]] - xy[ab[1]]))
tri = np.array([[0, 0], xy[i], xy[j]])
ax.fill(tri[:, 0], tri[:, 1], color=C_LOOP, alpha=0.17, zorder=2)
for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
    ax.plot(*zip(a, b), color=C_LOOP, lw=1.9, zorder=5, solid_capstyle="round")
ax.plot(*xy[[i, j]].T, "o", ms=6.5, color=C_LOOP, mec="white", mew=0.8, zorder=7)
ax.set_title(r"(a) $D_4$: $24$ links, $96$ triangles", fontsize=9.6)
ax.text(0, -1.72,
        r"chords $=$ elementary plaquettes" "\n"
        r"$\mathrm{Tr}\,U_{\triangle}=\mathrm{Tr}[U_{e}U_{f-e}U_{-f}]$",
        ha="center", va="top", fontsize=8.4, color=C_TXT)

# ------------------------------------------------------------------ (b)
ax = axes[1]
cols = [C_AX if a else C_DI for a in is_axial]
panel(ax, BCH_M, P_F4, 1.0, cols)
ax.set_title(r"(b) $D_4^{*}$: the same $24$ links", fontsize=9.6)
ax.text(0, -1.72,
        r"$8$ axial $+$ $16$ diagonal is a" "\n"
        r"coordinate split, not a gauge-invariant one",
        ha="center", va="top", fontsize=8.4, color=C_TXT)

# ------------------------------------------------------------------ (c)
ax = axes[2]
xy, n = panel(ax, HC * 1.256, P_B4, None, C_HC, ms=6.2)
assert n == 0
ax.set_title(r"(c) $\mathbb{Z}^4$: $8$ links, no triangles", fontsize=9.6)
ax.text(0, -1.72,
        "no chords: the lattice is bipartite\n"
        r"the minimal loop needs $4$ links",
        ha="center", va="top", fontsize=8.4, color=C_TXT)

for ax in axes:
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-2.35, 1.42)

fig.tight_layout(pad=0.5)
fig.savefig("../fig-d4-plaquettes.pdf")
fig.savefig("../fig-d4-plaquettes.png", dpi=200)
print("wrote fig-d4-plaquettes")

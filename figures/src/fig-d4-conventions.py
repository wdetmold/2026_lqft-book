"""D_4 conventions, figure 2: the same 24-cell in both normalisations, and the
self-duality that makes d=4 special.

(a) root convention   D_4  : 24 minimal vectors (+-1,+-1,0,0), |e|^2 = 2
(b) BCH convention    D_4* : 24 minimal vectors, 8 axial (+-1,0,0,0) plus
                             16 body diagonals (+-1/2,...), |e|^2 = 1
(c) shell 1 and shell 2 of D_4, each a 24-cell, in dual orientation:
    the geometric content of  D_4* ~ D_4.

Vertices are projected onto the Coxeter plane of Aut(D_4) = W(F_4), which has
Coxeter number 12; the picture therefore has 12-fold symmetry.
Panel (b) plots  sqrt(2) R v  with R the rotation carrying the BCH minimal
vectors onto the root-convention ones, so (a) and (b) are literally the same
polytope -- only the colouring, which is a coordinate artifact, differs.
"""
import itertools
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_A = "#0072B2"   # root convention / shell 1
C_AX = "#D55E00"  # BCH axial vectors
C_DI = "#009E73"  # BCH body diagonals
C_B = "#CC79A7"   # shell 2 (dual 24-cell)
C_ED = "#9DBEDC"  # edges

# ---------------------------------------------------------------- lattices
shell = lambda n2: np.array([v for v in itertools.product(range(-2, 3), repeat=4)
                             if sum(v) % 2 == 0 and sum(x * x for x in v) == n2], float)
S1, S2 = shell(2), shell(4)

BCH = ([np.array(v, float) for v in itertools.product((-1, 0, 1), repeat=4)
        if sum(x * x for x in v) == 1] +
       [np.array(s, float) * 0.5 for s in itertools.product((-1, 1), repeat=4)])
BCH = np.array(BCH)
is_axial = np.array([np.isclose(np.abs(v).max(), 1.0) for v in BCH])

R = np.array([[1, 1, 0, 0], [1, -1, 0, 0], [0, 0, 1, 1], [0, 0, 1, -1]]) / np.sqrt(2)
BCH_mapped = np.sqrt(2) * BCH @ R.T
assert {tuple(np.round(v).astype(int)) for v in BCH_mapped} == {tuple(v.astype(int)) for v in S1}

# ------------------------------------------------- Coxeter-plane projection
def coxeter_plane(vecs):
    """Plane on which a Coxeter element of the symmetry group acts by 2pi/12."""
    # Coxeter element of W(F_4): product of the four simple reflections.
    simple = np.array([[0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1], [.5, -.5, -.5, -.5]])
    M = np.eye(4)
    for r in simple:
        r = r / np.linalg.norm(r)
        M = (np.eye(4) - 2 * np.outer(r, r)) @ M
    w, V = np.linalg.eig(M)
    ang = np.angle(w)
    k = np.argmin(np.abs(ang - 2 * np.pi / 12))       # primitive 12th root
    z = V[:, k]
    u, v = np.real(z), np.imag(z)
    u /= np.linalg.norm(u); v -= (v @ u) * u; v /= np.linalg.norm(v)
    return np.vstack([u, v])
P = coxeter_plane(S1)
proj = lambda X: X @ P.T

def draw_polytope(ax, pts, cols, ip_edge, ms=6.0, edge_col=C_ED, lw=0.55, zo=3):
    xy = proj(pts)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if np.isclose(pts[i] @ pts[j], ip_edge):
                ax.plot(*zip(xy[i], xy[j]), color=edge_col, lw=lw, zorder=zo - 1)
    for i in range(len(pts)):
        ax.plot(*xy[i], "o", ms=ms, color=cols[i] if isinstance(cols, list) else cols,
                mec="white", mew=0.7, zorder=zo + 1)
    return xy

fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.35))

# --------------------------------------------------------------- (a) D_4
ax = axes[0]
draw_polytope(ax, S1, C_A, 1.0)
ax.set_title(r"(a) $D_4$: $(\pm1,\pm1,0,0)$", fontsize=10)
ax.text(0, -1.62, r"$24$ vectors, $|e|^2=2$" "\n" "one symmetry orbit",
        ha="center", va="top", fontsize=8.6, color="#444444")

# --------------------------------------------------------------- (b) D_4*
ax = axes[1]
cols = [C_AX if a else C_DI for a in is_axial]
draw_polytope(ax, BCH_mapped, cols, 1.0)
ax.set_title(r"(b) $D_4^{*}$: $(\pm1,0,0,0)\ \oplus\ (\pm\frac{1}{2},\dots)$", fontsize=10)
ax.text(0, -1.62,
        r"$8$ axial $+$ $16$ diagonal, $|e|^2=1$" "\n" "still one orbit: triality mixes them",
        ha="center", va="top", fontsize=8.6, color="#444444")

# --------------------------------------------------------------- (c) duality
ax = axes[2]
draw_polytope(ax, S1, C_A, 1.0, ms=5.5)
S2n = S2 / np.sqrt(2)
xy2 = proj(S2n)
for i in range(len(S2n)):
    ax.plot(*xy2[i], "s", ms=5.4, color=C_B, mec="white", mew=0.8, zorder=6)
ax.set_title(r"(c) shell 1 and shell 2 of $D_4$", fontsize=10)
ax.text(0, -1.62,
        "two interlocking $24$-cells\n" r"the self-duality $D_4^{*}\simeq D_4$",
        ha="center", va="top", fontsize=8.6, color="#444444")

for ax in axes:
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.55, 1.55); ax.set_ylim(-2.18, 1.45)

fig.tight_layout(pad=0.5)
fig.savefig("../fig-d4-conventions.pdf")
fig.savefig("../fig-d4-conventions.png", dpi=200)
print("wrote fig-d4-conventions")

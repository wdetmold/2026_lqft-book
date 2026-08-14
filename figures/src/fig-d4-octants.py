"""D_4 gauge theory: why there is no checkerboard, and what replaces it.

The 24 link directions of D_4 fall into three classes of eight, indexed by the
three ways of splitting {1,2,3,4} into two complementary coordinate planes:

    A = planes (12),(34)     B = planes (13),(24)     C = planes (14),(23)

Two vectors of the same class never sum to a minimal vector, so no triangle
contains two links of the same class: every one of the 96 triangles through a
site takes exactly one link from each class.  Consequently all links of one
class can be updated simultaneously -- a three-sweep scheme that needs no site
parity, unlike the hypercubic checkerboard.  Aut(D_4) permutes the three
classes as S_3 = Aut(D_4)/W(D_4), i.e. exactly by triality.

(a) the 24 links coloured by class, with the triangle chords drawn
(b) one triangle: one link from each class
"""
import itertools
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

COL = {"A": "#0072B2", "B": "#D55E00", "C": "#009E73"}
C_CH = "#C9D6E0"

S = np.array([v for v in itertools.product((-1, 0, 1), repeat=4)
              if sum(v) % 2 == 0 and sum(x * x for x in v) == 2], float)
CL = {"A": [(0, 1), (2, 3)], "B": [(0, 2), (1, 3)], "C": [(0, 3), (1, 2)]}


def cls(v):
    idx = tuple(sorted(i for i in range(4) if abs(v[i]) > 1e-9))
    for n, pl in CL.items():
        if idx in pl:
            return n


def coxeter_plane():
    simple = np.array([[0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 0, 1],
                       [.5, -.5, -.5, -.5]])
    M = np.eye(4)
    for r in simple:
        r = r / np.linalg.norm(r)
        M = (np.eye(4) - 2 * np.outer(r, r)) @ M
    w, V = np.linalg.eig(M)
    k = np.argmin(np.abs(np.angle(w) - 2 * np.pi / 12))
    z = V[:, k]
    u, v = np.real(z), np.imag(z)
    u /= np.linalg.norm(u); v -= (v @ u) * u; v /= np.linalg.norm(v)
    return np.vstack([u, v])


P = coxeter_plane()
xy = S @ P.T
cols = [COL[cls(v)] for v in S]

fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.6))

# ------------------------------------------------------------------ (a)
ax = axes[0]
for i in range(len(S)):
    ax.plot([0, xy[i, 0]], [0, xy[i, 1]], color="#E2E8EE", lw=0.6, zorder=0)
for i in range(len(S)):
    for j in range(i + 1, len(S)):
        if np.isclose(S[i] @ S[j], 1.0):
            ax.plot(*zip(xy[i], xy[j]), color=C_CH, lw=0.55, zorder=1)
for i in range(len(S)):
    ax.plot(*xy[i], "o", ms=6.4, color=cols[i], mec="white", mew=0.8, zorder=4)
ax.plot(0, 0, "o", ms=6.5, color="#333333", zorder=6)
for k, (name, lab) in enumerate((("A", "(12),(34)"), ("B", "(13),(24)"),
                                 ("C", "(14),(23)"))):
    x0 = -1.55 + k * 1.10
    ax.plot(x0, 1.62, "o", ms=6.0, color=COL[name], mec="white", mew=0.7)
    ax.text(x0 + 0.12, 1.62, lab, color=COL[name], fontsize=8.2,
            ha="left", va="center")
ax.set_title(r"(a) the $24$ links in three classes of $8$", fontsize=9.8)
ax.text(0, -1.95, "every chord joins two different classes",
        ha="center", va="top", fontsize=8.5, color="#444444")

# ------------------------------------------------------------------ (b)
ax = axes[1]
for i in range(len(S)):
    ax.plot([0, xy[i, 0]], [0, xy[i, 1]], color="#EDF1F4", lw=0.55, zorder=0)
    ax.plot(*xy[i], "o", ms=4.2, color="#D7DEE4", mec="white", mew=0.5, zorder=2)
cand = [(a, b) for a in range(len(S)) for b in range(len(S))
        if a < b and np.isclose(S[a] @ S[b], 1.0)]
i, j = max(cand, key=lambda ab: np.linalg.norm(xy[ab[0]] - xy[ab[1]]))
tri = np.array([[0, 0], xy[i], xy[j]])
ax.fill(tri[:, 0], tri[:, 1], color="#F2C9A0", alpha=0.30, zorder=1)
e_i, e_j = S[i], S[j]
segs = [((0, 0), xy[i], cls(e_i)), (xy[i], xy[j], cls(e_j - e_i)),
        (xy[j], (0, 0), cls(e_j))]
for a, b, c in segs:
    ax.plot(*zip(a, b), color=COL[c], lw=2.6, zorder=5, solid_capstyle="round")
ax.plot(*xy[[i, j]].T, "o", ms=6.6, color="#333333", mec="white", mew=0.8, zorder=7)
ax.plot(0, 0, "o", ms=6.6, color="#333333", zorder=7)
mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
for (a, b, c), off in zip(segs, ((-0.20, 0.10), (0.22, 0.02), (0.02, -0.24))):
    m = mid(np.asarray(a, float), np.asarray(b, float))
    ax.text(m[0] + off[0], m[1] + off[1], c, color=COL[c], fontsize=10.5,
            ha="center", va="center", fontweight="bold")
ax.set_title(r"(b) one triangle, one link per class", fontsize=9.8)
ax.text(0, -1.95,
        "so a whole class updates in parallel:\n"
        "three sweeps, and no site parity needed",
        ha="center", va="top", fontsize=8.5, color="#444444")

for ax in axes:
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.85, 1.85); ax.set_ylim(-2.65, 1.85)

fig.tight_layout(pad=0.5)
fig.savefig("../fig-d4-octants.pdf")
fig.savefig("../fig-d4-octants.png", dpi=200)
print("wrote fig-d4-octants")

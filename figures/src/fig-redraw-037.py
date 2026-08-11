"""Redraw of fig-notes-037: visual representation of the allowed
finite-volume energies.  Branches of the 3D zeta function
S(p~) = sum_n 1/(|n|^2 - p~^2) - 4 pi Lambda_n  (poles at p~^2 = 0,1,2,...)
are intersected by p cot(delta), shown for a scattering-length-only model
(blue) and an effective-range model (red); the intersections are the
allowed finite-volume energies."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"
C_GREEN = "#009E73"

# ---- regulated zeta function S(eta), eta = p~^2 --------------------------
LAM = 60
r = np.arange(-LAM, LAM + 1)
X, Y, Z = np.meshgrid(r, r, r, indexing="ij", sparse=True)
n2 = (X * X + Y * Y + Z * Z).ravel()
n2 = n2[n2 <= LAM * LAM]
counts = np.bincount(n2)
kk = np.arange(len(counts), dtype=float)

def S(eta):
    eta = np.atleast_1d(np.asarray(eta, dtype=float))
    return (counts[None, :] / (kk[None, :] - eta[:, None])).sum(axis=1) \
        - 4 * np.pi * LAM

XMIN, XMAX = -0.85, 5.45
YMIN, YMAX = -42.0, 52.0
poles = [0, 1, 2, 3, 4, 5]

# the two p cot delta models (schematic units: overall pi*L scaling implicit)
c_blue = 15.0                       # p cot d = -1/a
red = lambda x: 6.0 + 8.0 * x       # p cot d = -1/a + (r/2) p^2

fig, ax = plt.subplots(figsize=(6.0, 3.0))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)

# zeta-function branches (split at the poles)
edges = [XMIN] + [p for p in poles if XMIN < p < XMAX] + [XMAX]
for a, b in zip(edges[:-1], edges[1:]):
    x = np.linspace(a + 1e-3, b - 1e-3, 500)
    y = S(x)
    y = np.where(np.abs(y) > 1.2e3, np.nan, y)
    ax.plot(x, y, color=C_GREEN, lw=1.3, zorder=2)

# p cot delta models
ax.axhline(c_blue, color=C_BLUE, lw=1.6, zorder=3)
xr = np.linspace(XMIN, XMAX, 10)
ax.plot(xr, red(xr), color=C_RED, lw=1.6, zorder=3)

# intersections = allowed finite-volume energies (found per branch)
def crossings(f):
    pts = []
    for a, b in zip(edges[:-1], edges[1:]):
        x = np.linspace(a + 1e-4, b - 1e-4, 4000)
        d = S(x) - f(x)
        s = np.where(np.diff(np.sign(d)) != 0)[0]
        for i in s:
            pts.append(0.5 * (x[i] + x[i + 1]))
    return np.array(pts)

xb = crossings(lambda x: np.full_like(x, c_blue))
ax.plot(xb, np.full_like(xb, c_blue), ls="none", marker="o", ms=5.5,
        mfc="white", mec=C_BLUE, mew=1.3, zorder=5)
xr_c = crossings(red)
ax.plot(xr_c, red(xr_c), ls="none", marker="o", ms=5, color=C_RED, zorder=5)

# centered, arrowed axes
for side in ["top", "right", "left", "bottom"]:
    ax.spines[side].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.annotate("", xy=(XMAX, 0), xytext=(XMIN, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0), zorder=1)
ax.annotate("", xy=(0, YMAX), xytext=(0, YMIN),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0), zorder=1)
for p in [1, 2, 3, 4, 5]:
    ax.plot([p, p], [-1.8, 1.8], color="k", lw=0.9, zorder=1)
    ax.text(p + 0.07, -3.5, str(p), ha="left", va="top", fontsize=9)

# labels (model labels sit at the right-hand ends of their lines)
ax.text(-0.1, 48, r"$S(\tilde{p})$", ha="right", va="center",
        color=C_GREEN, fontsize=11)
ax.text(XMAX, -46, r"$\tilde{p}^{\,2} = \frac{L^2}{4\pi^2}p^2$",
        ha="right", va="top", fontsize=11)
ax.text(XMAX + 0.1, red(XMAX), r"$p\cot\delta(p) = -\frac{1}{a} + \frac{r}{2}p^2$",
        ha="left", va="center", color=C_RED, fontsize=9.5)
ax.text(XMAX + 0.1, c_blue, r"$p\cot\delta(p) = -\frac{1}{a}$",
        ha="left", va="center", color=C_BLUE, fontsize=9.5)

fig.savefig("../fig-redraw-037.pdf")
fig.savefig("../fig-redraw-037.png", dpi=200)

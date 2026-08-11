"""Redraw of fig-notes-036 (first panel of fig:int_spec): two-particle
finite-volume spectrum as a function of the lattice size L.  The lowest
level is flat at 2 m_pi; excited levels fall like the free momentum modes.
Levels realised at two sizes L_1 < L_2 are marked (they reappear in the
density-of-states panels, figs 034 and 035)."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"
C_PURPLE = "#CC79A7"

M_PI = 0.5
def E_n(n, L):
    return 2.0 * np.sqrt(M_PI**2 + n * (2 * np.pi / L)**2)

L1, L2 = 3.8, 9.0
LMIN, LMAX = 2.8, 12.0
YMAX = 5.6

fig, ax = plt.subplots(figsize=(3.4, 2.8))
ax.set_xlim(0, LMAX + 0.7)
ax.set_ylim(0, YMAX + 0.4)
ax.axis("off")

# arrowed axes
ax.annotate("", xy=(LMAX + 0.7, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, YMAX + 0.4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0))
ax.text(-0.45, YMAX + 0.1, r"$E$", ha="right", va="center", fontsize=12)
ax.text(LMAX + 0.55, -0.55, r"$L$", ha="center", va="top", fontsize=12)

# energy levels vs L
L = np.linspace(LMIN, LMAX, 400)
for n in range(5):
    y = E_n(n, L)
    m = y <= YMAX
    ax.plot(L[m], y[m], color=C_BLUE, lw=1.6, zorder=3)

# levels realised at L_1 (dots) and L_2 (crosses)
for n in range(5):
    y1 = E_n(n, L1)
    if y1 <= YMAX:
        ax.plot([L1], [y1], marker="o", ms=5, color=C_RED, ls="none", zorder=5)
    y2 = E_n(n, L2)
    if y2 <= YMAX:
        ax.plot([L2], [y2], marker="x", ms=6, mew=1.6, color=C_PURPLE,
                ls="none", zorder=5)

# ticks for L_1 and L_2
for Lx, c, s in [(L1, C_RED, r"$L_1$"), (L2, C_PURPLE, r"$L_2$")]:
    ax.plot([Lx, Lx], [-0.09, 0.09], color=c, lw=1.4, clip_on=False)
    ax.text(Lx, -0.35, s, ha="center", va="top", color=c, fontsize=11)

fig.savefig("../fig-redraw-036.pdf")
fig.savefig("../fig-redraw-036.png", dpi=200)

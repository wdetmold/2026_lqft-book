"""Redraw of fig-notes-038 (first panel of fig:resonance): spectrum of the
two-scalar model at coupling g = 0.  The rho level (dashed, at m_rho) and
the phi-phi threshold (dashed, at 2 m_phi) are flat in L; the free two-phi
momentum levels fall with L and cross the rho level without mixing.
Open circles mark the levels at a set of lattice sizes."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"
C_GREEN = "#009E73"

M_PHI = 0.5
M_RHO = 2.2
def E_n(n, L):
    return 2.0 * np.sqrt(M_PHI**2 + n * (2 * np.pi / L)**2)

LMIN, LMAX = 2.8, 12.0
YMAX = 4.5
L_pts = np.array([3.5, 5.0, 6.5, 8.0, 9.5, 11.0])

fig, ax = plt.subplots(figsize=(3.4, 3.0))
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
ax.text(-0.45, YMAX + 0.15, r"$E$", ha="right", va="center", fontsize=12)
ax.text(LMAX + 0.55, -0.5, r"$L$", ha="center", va="top", fontsize=12)

# flat reference levels: rho and two-phi threshold
ax.plot([LMIN, LMAX], [M_RHO, M_RHO], color=C_RED, ls="--", lw=1.4, zorder=2)
ax.plot([LMIN, LMAX], [2 * M_PHI, 2 * M_PHI], color=C_BLUE, ls="--", lw=1.4,
        zorder=2)
ax.text(LMAX + 0.25, M_RHO, r"$m_\rho$", ha="left", va="center",
        color=C_RED, fontsize=10)
ax.text(LMAX + 0.25, 2 * M_PHI, r"$2m_\phi$", ha="left", va="center",
        color=C_BLUE, fontsize=10)

# free two-phi momentum levels
L = np.linspace(LMIN, LMAX, 400)
for n in (1, 2, 3):
    y = E_n(n, L)
    m = y <= YMAX
    ax.plot(L[m], y[m], color=C_BLUE, lw=1.6, zorder=3)

# levels measured at a set of lattice sizes
ax.plot(L_pts, np.full_like(L_pts, M_RHO), ls="none", marker="o", ms=4.5,
        mfc="white", mec=C_RED, mew=1.2, zorder=5)
ax.plot(L_pts, np.full_like(L_pts, 2 * M_PHI), ls="none", marker="o", ms=4.5,
        mfc="white", mec=C_BLUE, mew=1.2, zorder=5)
for n in (1, 2, 3):
    y = E_n(n, L_pts)
    m = y <= YMAX
    ax.plot(L_pts[m], y[m], ls="none", marker="o", ms=4.5, mfc="white",
            mec=C_BLUE, mew=1.2, zorder=5)

ax.text(0.55 * LMAX, YMAX + 0.15, r"$g = 0$", ha="center", va="center",
        color=C_GREEN, fontsize=12)

fig.savefig("../fig-redraw-038.pdf")
fig.savefig("../fig-redraw-038.png", dpi=200)

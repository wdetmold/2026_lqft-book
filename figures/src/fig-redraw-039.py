"""Redraw of fig-notes-039 (second panel of fig:resonance): spectrum of the
two-scalar model at coupling g > 0.  The rho state mixes with the two-phi
levels, producing avoided level crossings: levels plateau near m_rho
instead of crossing it.  Dashed lines mark m_rho and 2 m_phi; open circles
mark the levels at a set of lattice sizes."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"
C_GREEN = "#009E73"

M_PHI = 0.5
M_RHO = 2.2
G = 0.16       # rho <-> phi-phi coupling
C3 = 6.0       # small repulsive 1/L^3 shift of the two-phi levels

def free_levels(L):
    lev = [2.0 * np.sqrt(M_PHI**2 + n * (2 * np.pi / L)**2) + C3 / L**3
           for n in range(4)]
    return np.array(lev)

def spectrum(L):
    """Eigenvalues of {rho} + {phi-phi levels} with coupling G."""
    E = free_levels(L)
    H = np.diag(np.concatenate(([M_RHO], E)))
    H[0, 2:] = H[2:, 0] = G   # rho mixes with the moving phi-phi levels
    return np.sort(np.linalg.eigvalsh(H))

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

# flat reference levels: rho mass and two-phi threshold
ax.plot([LMIN, LMAX], [M_RHO, M_RHO], color=C_RED, ls="--", lw=1.4, zorder=1)
ax.plot([LMIN, LMAX], [2 * M_PHI, 2 * M_PHI], color=C_BLUE, ls="--", lw=1.4,
        zorder=1)
ax.text(LMAX + 0.25, M_RHO, r"$m_\rho$", ha="left", va="center",
        color=C_RED, fontsize=10)
ax.text(LMAX + 0.25, 2 * M_PHI, r"$2m_\phi$", ha="left", va="center",
        color=C_BLUE, fontsize=10)

# interacting spectrum: avoided level crossings
L = np.linspace(LMIN, LMAX, 500)
spec = np.array([spectrum(Li) for Li in L])   # (nL, 5)
for i in range(spec.shape[1]):
    y = spec[:, i]
    m = y <= YMAX
    ax.plot(L[m], y[m], color=C_BLUE, lw=1.6, zorder=3)

# levels measured at a set of lattice sizes
for Li in L_pts:
    y = spectrum(Li)
    y = y[y <= YMAX]
    ax.plot(np.full_like(y, Li), y, ls="none", marker="o", ms=4.5,
            mfc="white", mec=C_BLUE, mew=1.2, zorder=5)

ax.text(0.55 * LMAX, YMAX + 0.15, r"$g > 0$", ha="center", va="center",
        color=C_GREEN, fontsize=12)

fig.savefig("../fig-redraw-039.pdf")
fig.savefig("../fig-redraw-039.png", dpi=200)

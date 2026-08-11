"""Redraw of fig-notes-022: bare-parameter space (beta, kappa) of the Wilson
gauge + fermion action for a single quark flavour.

Shows the critical line kappa_c (m_q = 0), a curve of constant physics
(e.g. M_pi/M_N fixed) ending at kappa_phys in the continuum limit, and
dotted curves of constant lattice spacing.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_RED = "#D55E00"    # kappa_c line
C_BLUE = "#0072B2"   # curve of constant physics
C_GREEN = "#009E73"  # curves of constant lattice spacing

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# x in [0, 1] maps beta = 0 ... infinity; y = kappa
x = np.linspace(0.0, 1.0, 300)

# critical line kappa_c(beta): m_q = 0, from 1/4 at beta=0 to 1/8 at beta=inf
kc = PchipInterpolator(
    [0.00, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.00],
    [0.250, 0.248, 0.240, 0.222, 0.196, 0.168, 0.146, 0.135])
ax.plot(x, kc(x), color=C_RED, lw=1.8, zorder=3)

# curve of constant physics, ending at kappa_phys at beta = infinity
xb = np.linspace(0.20, 1.0, 200)
kp = PchipInterpolator(
    [0.20, 0.32, 0.45, 0.58, 0.72, 0.86, 1.00],
    [0.048, 0.072, 0.088, 0.097, 0.101, 0.103, 0.104])
ax.plot(xb, kp(xb), color=C_BLUE, lw=1.8, zorder=3)

# simulation points on the curve of constant physics (circled crosses)
xs = np.array([0.27, 0.41, 0.56, 0.68])
ax.plot(xs, kp(xs), ls="none", marker="o", ms=7, mfc="white",
        mec=C_BLUE, mew=1.2, zorder=4)
ax.plot(xs, kp(xs), ls="none", marker="x", ms=4.5, color=C_BLUE,
        mew=1.2, zorder=5)

# continuum-limit endpoint kappa_phys
ax.plot([1.0], [kp(1.0)], marker="o", ms=5, color=C_BLUE,
        zorder=5, clip_on=False)

# dotted curves of constant lattice spacing (nearly vertical)
for x0 in [0.24, 0.36, 0.48, 0.60, 0.72]:
    yy = np.linspace(0.015, 0.215, 50)
    xx = x0 + 0.055 * (yy - 0.015) / 0.20
    ax.plot(xx, yy, color=C_GREEN, lw=1.1, ls=(0, (1.5, 2.0)), zorder=2)

# ---- direct labels ---------------------------------------------------------
ax.text(0.52, 0.230, r"$\kappa_c:\ m_q = 0$", color=C_RED,
        ha="center", va="bottom", fontsize=11)
ax.text(0.045, 0.155, "curves of\nconstant\nlattice spacing", color=C_GREEN,
        ha="left", va="center", fontsize=9)
ax.text(0.56, 0.044, "curve of constant physics,\ne.g. $M_\\pi/M_N$ fixed",
        color=C_BLUE, ha="center", va="top", fontsize=9, zorder=6,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))

# right-edge labels for the two limiting kappa values
ax.text(1.02, kc(1.0), r"$\kappa = \frac{1}{8}$", color=C_RED,
        ha="left", va="center", fontsize=10, clip_on=False)
ax.text(1.02, kp(1.0), r"$\kappa = \kappa_{\mathrm{phys}}$", color=C_BLUE,
        ha="left", va="center", fontsize=10, clip_on=False)

# ---- axes ------------------------------------------------------------------
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.30)
ax.set_xticks([0, 1])
ax.set_xticklabels([r"$\beta = 0$", r"$\beta = \infty$"])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([r"$\kappa = 0$", r"$\kappa = \frac{1}{4}$"])
ax.minorticks_off()
ax.tick_params(length=0)
# keep the corner labels kappa=0 and beta=0 from colliding
ax.get_yticklabels()[0].set_verticalalignment("bottom")
ax.get_xticklabels()[0].set_horizontalalignment("left")
ax.set_xlabel(r"$\beta$")
ax.set_ylabel(r"$\kappa$")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-022.pdf")
fig.savefig("../fig-redraw-022.png", dpi=200)
print("done 022")

import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of the figural content of fig-notes-094.pdf (handwritten notes page):
# the small (lambda, kappa) sketch showing where the hopping (kappa)
# expansion is valid. Critical line kappa_c(lambda) between lambda = 0 and
# lambda = infinity; the expansion is valid for small lambda (vertical band)
# and, in the symmetric phase, for kappa <= kappa_c (horizontal band).
# The equations on the notes page are already transcribed in the tex.

import numpy as np
from scipy.interpolate import PchipInterpolator

C_CURVE = "#0072B2"   # critical line
C_SMALL = "#D55E00"   # small-lambda band annotation
C_SYMM = "#009E73"    # symmetric-phase band annotation

fig, ax = plt.subplots(figsize=(4.6, 3.0))

# critical line kappa_c(lambda), x in [0,1] maps lambda = 0..infinity
x = np.linspace(0.0, 1.0, 300)
kc = PchipInterpolator(
    [0.00, 0.15, 0.35, 0.55, 0.75, 0.90, 1.00],
    [0.125, 0.141, 0.150, 0.145, 0.121, 0.094, 0.07475])
ax.plot(x, kc(x), color=C_CURVE, lw=1.8, zorder=3)
ax.plot(1.0, kc(1.0), "o", color=C_CURVE, ms=4, zorder=4)

# kappa = 0 line and the lambda = infinity boundary
ax.axhline(0.0, color="0.35", lw=0.9, ls=(0, (5, 4)), zorder=2)
ax.axvline(1.0, color="0.55", lw=0.8, zorder=1)

# validity bands
ax.axvspan(0.0, 0.07, color="#D55E00", alpha=0.14, lw=0, zorder=0)
ax.axhspan(0.0, kc(1.0), color="#009E73", alpha=0.14, lw=0, zorder=0)

ax.annotate(r"valid for small $\lambda$", xy=(0.05, 0.163),
            xytext=(0.24, 0.180), color=C_SMALL, fontsize=9.5,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C_SMALL, lw=0.9,
                            connectionstyle="arc3,rad=0.25",
                            shrinkA=2, shrinkB=2))
ax.annotate("valid in symmetric phase\nfor $\\kappa \\leq \\kappa_c$",
            xy=(0.93, 0.045), xytext=(0.62, -0.045), color=C_SYMM,
            fontsize=9.5, ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C_SYMM, lw=0.9,
                            connectionstyle="arc3,rad=-0.25",
                            shrinkA=2, shrinkB=2))
ax.text(0.35, 0.115, r"$\kappa_c(\lambda)$", color=C_CURVE, ha="center",
        va="bottom", fontsize=10)

ax.set_xlim(0, 1)
ax.set_ylim(-0.075, 0.195)
ax.set_xticks([0, 1])
ax.set_xticklabels(["$0$", r"$\infty$"])
ax.set_yticks([0])
ax.set_yticklabels(["$0$"])
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$\kappa$", rotation=0, labelpad=8)
ax.minorticks_off()
ax.tick_params(length=0)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)

fig.savefig("../fig-redraw-094.pdf")
fig.savefig("../fig-redraw-094.png", dpi=200)

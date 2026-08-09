"""Redraw of fig-notes-004: region of the O(n) phase diagram studied in the
weak coupling expansion -- a band at small lambda in the (lambda, kappa)
plane, below the critical line kappa_c(lambda).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_CURVE = "#0072B2"   # critical line
C_ANN = "#D55E00"     # annotation
C_BAND = "#CC79A7"    # shaded region

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# x in [0,1] maps lambda = 0 .. infinity; critical line as in the phase
# diagram figure (1/8 at lambda = 0, 0.07475... at lambda = infinity).
x = np.linspace(0.0, 1.0, 300)
kc = PchipInterpolator(
    [0.00, 0.15, 0.35, 0.55, 0.75, 0.90, 1.00],
    [0.125, 0.141, 0.150, 0.145, 0.121, 0.094, 0.07475])
ax.plot(x, kc(x), color=C_CURVE, lw=1.8, zorder=3)
ax.text(0.47, 0.158, r"$\kappa_c(\lambda)$", color=C_CURVE,
        ha="center", va="bottom", fontsize=10)

ax.axhline(0.0, color="0.35", lw=0.9, ls=(0, (5, 4)), zorder=1)
ax.axvline(1.0, color="0.55", lw=0.8, zorder=1)

# shaded band at small lambda where the expansion is valid
ax.axvspan(0.0, 0.12, color=C_BAND, alpha=0.25, lw=0, zorder=0)
ax.annotate(r"valid for small $\lambda$", xy=(0.09, 0.185),
            xytext=(0.34, 0.208), color=C_ANN, fontsize=10,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C_ANN, lw=0.9,
                            shrinkA=2, shrinkB=2))

ax.set_xlim(0, 1)
ax.set_ylim(-0.035, 0.225)
ax.set_xticks([0, 1])
ax.set_xticklabels(["$0$", r"$\infty$"])
ax.set_yticks([0])
ax.set_yticklabels(["$0$"])
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$\kappa$", rotation=0, labelpad=8)
ax.minorticks_off()
ax.tick_params(length=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.savefig("../fig-redraw-004.pdf")
fig.savefig("../fig-redraw-004.png", dpi=200)

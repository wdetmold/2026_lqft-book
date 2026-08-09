"""Redraw of fig-notes-023: conjectured QCD phase diagram in the
(baryon chemical potential, temperature) plane.

Crossover at low mu_B ending in a critical end point, first-order line
down to the mu_B axis, hadronic phase / quark-gluon plasma, nuclei and
neutron-star matter on the axis, and (beyond an axis break) the
colour-flavour locked superconducting state known from asymptotic freedom.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_BLUE = "#0072B2"   # phase boundaries and phase labels
C_RED = "#D55E00"    # annotations
C_GRAY = "#888888"   # axis-break marks

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.axis("off")
ax.set_xlim(-1.6, 11.1)
ax.set_ylim(-2.0, 10.2)
ax.set_aspect("auto")

arrow = dict(arrowstyle="-|>", color="black", lw=0.9,
             shrinkA=0, shrinkB=0, mutation_scale=12)

# ---- axes with arrowheads --------------------------------------------------
ax.annotate("", xy=(0, 9.6), xytext=(0, 0), arrowprops=arrow)
ax.annotate("", xy=(10.3, 0), xytext=(0, 0), arrowprops=arrow)
ax.text(-0.45, 9.4, r"$T$", ha="right", va="center", fontsize=12)
ax.text(10.25, -0.75, r"$\mu_B$", ha="center", va="top", fontsize=12)

# T ~ 155 MeV mark on the T axis
ax.plot([-0.13, 0.13], [6.0, 6.0], color="black", lw=0.9)
ax.text(-0.35, 6.0, r"$\sim 155\ \mathrm{MeV}$", ha="right", va="center",
        fontsize=9)

# ---- crossover line (dashed) ending in the critical end point --------------
xc = np.linspace(0, 2.6, 60)
yc = PchipInterpolator([0, 1.0, 1.8, 2.6], [6.0, 5.9, 5.7, 5.4])(xc)
ax.plot(xc, yc, color=C_BLUE, lw=1.6, ls=(0, (4, 3)), zorder=3)
ax.plot([2.6], [5.4], marker="o", ms=7, color=C_BLUE, zorder=4)

# ---- first-order line from the CEP down to the mu_B axis -------------------
yf = np.linspace(0, 5.4, 80)
xf = PchipInterpolator([0.0, 1.5, 3.0, 4.5, 5.4],
                       [3.95, 3.88, 3.62, 3.05, 2.60])(yf)
ax.plot(xf, yf, color=C_BLUE, lw=1.8, zorder=3)

# ---- uncertain region at low T, larger mu_B --------------------------------
ax.plot([4.35, 6.35], [1.75, 1.85], color=C_BLUE, lw=1.4,
        ls=(0, (1.5, 2.5)), zorder=3)
ax.text(5.65, 2.35, r"$?$", color=C_BLUE, fontsize=13, ha="center")
ax.text(6.35, 2.55, r"$?$", color=C_BLUE, fontsize=13, ha="center")

# ---- axis break before the asymptotically large mu_B region ----------------
ax.add_patch(plt.Polygon([(6.75, -0.6), (7.55, 9.6), (8.05, 9.6),
                          (7.25, -0.6)], closed=True, facecolor="white",
                         edgecolor="none", zorder=5))
ax.plot([6.75, 7.55], [-0.6, 9.6], color=C_GRAY, lw=1.0, zorder=6)
ax.plot([7.25, 8.05], [-0.6, 9.6], color=C_GRAY, lw=1.0, zorder=6)

# ---- colour-flavour locked state at asymptotically large mu_B --------------
ax.plot([8.35, 10.7], [2.6, 2.6], color=C_BLUE, lw=1.8, zorder=3)
ax.text(9.5, 2.15, "colour-flavour locked\nsuperconducting state",
        color=C_BLUE, ha="center", va="top", fontsize=8.5, zorder=8)

# ---- phase labels ----------------------------------------------------------
ax.text(2.3, 8.3, "quark-gluon\nplasma", color=C_BLUE, ha="center",
        va="center", fontsize=10)
ax.text(1.25, 2.85, "hadrons", color=C_BLUE, ha="center", va="center",
        fontsize=10)

# ---- red annotations with arrows -------------------------------------------
ann = dict(arrowstyle="-|>", color=C_RED, lw=0.9, shrinkA=2, shrinkB=2,
           mutation_scale=10)
ax.annotate("crossover", xy=(0.95, 5.98), xytext=(1.75, 7.15),
            color=C_RED, fontsize=9, ha="left", va="center",
            arrowprops=dict(connectionstyle="arc3,rad=0.15", **ann))
ax.annotate("critical\nend point", xy=(2.42, 5.22), xytext=(1.15, 4.35),
            color=C_RED, fontsize=9, ha="center", va="center",
            arrowprops=dict(connectionstyle="arc3,rad=0.2", **ann))
ax.annotate("first-order\ntransition", xy=(3.25, 4.75), xytext=(4.75, 5.6),
            color=C_RED, fontsize=9, ha="center", va="center",
            arrowprops=dict(connectionstyle="arc3,rad=-0.2", **ann))
ax.annotate("known from\nasymptotic freedom", xy=(9.55, 2.75),
            xytext=(9.45, 4.9), color=C_RED, fontsize=8.5, ha="center",
            va="center", zorder=8,
            arrowprops=dict(connectionstyle="arc3,rad=-0.25", **ann))

# ---- matter on the mu_B axis -----------------------------------------------
ann_b = dict(arrowstyle="-|>", color=C_BLUE, lw=0.9, shrinkA=2, shrinkB=2,
             mutation_scale=10)
ax.annotate("nuclei", xy=(3.5, -0.12), xytext=(2.85, -1.35),
            color=C_BLUE, fontsize=9, ha="center", va="center",
            arrowprops=dict(connectionstyle="arc3,rad=0.2", **ann_b))
ax.annotate("neutron\nstars", xy=(5.35, -0.12), xytext=(5.75, -1.35),
            color=C_BLUE, fontsize=9, ha="center", va="center",
            arrowprops=dict(connectionstyle="arc3,rad=-0.2", **ann_b))

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-023.pdf")
fig.savefig("../fig-redraw-023.png", dpi=200)
print("done 023")

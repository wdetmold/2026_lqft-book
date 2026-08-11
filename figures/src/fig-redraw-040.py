"""Redraw of fig-notes-040: beta function of a walking-technicolour theory.

beta(g) leaves the UV (Gaussian) fixed point at g = 0, dips down QCD-like,
then comes back up almost touching zero at g = g_* (approximate IR fixed
point, red dot on the axis) before turning down again. A red dotted branch
continues the QCD-like fall for comparison. Schematic; arbitrary units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator
from scipy.interpolate import PchipInterpolator

CBLUE = "#0072B2"
CRED = "#D55E00"

GSTAR = 1.0

# Walking beta function: dip, near-touch of zero at g_*, dip again.
g_anchor = [0.0, 0.15, 0.40, 0.62, 0.85, GSTAR, 1.15, 1.32]
b_anchor = [0.0, -0.06, -0.48, -0.72, -0.34, -0.045, -0.34, -0.80]
f = PchipInterpolator(g_anchor, b_anchor)
g = np.linspace(0, 1.32, 500)

# QCD-like continuation from the dip region (dotted).
gq_anchor = [0.62, 0.80, 0.95, 1.08]
bq_anchor = [-0.72, -0.88, -1.05, -1.22]
fq = PchipInterpolator(gq_anchor, bq_anchor)
gq = np.linspace(0.62, 1.08, 200)

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(g, f(g), color=CBLUE, lw=1.8, zorder=3)
ax.plot(gq, fq(gq), color=CRED, lw=1.4, ls=":", zorder=2)
ax.text(0.97, -1.18, "QCD-like", color=CRED, fontsize=10, ha="right", va="top")

# UV fixed point at the origin.
ax.plot(0, 0, "o", ms=5, color=CRED, zorder=4, clip_on=False)
ax.text(0.10, 0.14, "UV fixed point", color=CRED, fontsize=10, ha="left")

# Approximate IR fixed point at g_*.
ax.plot(GSTAR, 0, "o", ms=5, color=CRED, zorder=4)
ax.plot([GSTAR, GSTAR], [0, -0.045], color=CRED, lw=1.2, ls=":", zorder=2)
ax.text(1.06, 0.26, "IR fixed point", color=CRED, fontsize=10, ha="center")
ax.text(GSTAR, 0.09, r"$g_*$", color=CRED, fontsize=11, ha="center")

ax.set_xlim(0, 1.38)
ax.set_ylim(-1.28, 0.40)
ax.text(1.36, -0.09, r"$g$", fontsize=12, ha="right", va="top")
ax.set_ylabel(r"$\beta(g)$", rotation=0, labelpad=14)
ax.yaxis.set_label_coords(-0.03, 0.90)

ax.set_xticks([])
ax.set_yticks([])
ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_minor_locator(NullLocator())

# Schematic axes: x axis at beta = 0 with arrow, y axis on the left.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_position(("data", 0.0))
ax.plot(1, 0.0, ">k", ms=5, transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", ms=5, transform=ax.get_xaxis_transform(), clip_on=False)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-040.pdf")
fig.savefig("../fig-redraw-040.png", dpi=200)
print("done")

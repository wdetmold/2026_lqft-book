"""Redraw of fig-notes-041: perturbative beta functions and IR fixed points.

Trajectories of beta(g) for different numbers of colours/flavours:
  - beta_0 < 0: beta rises from zero (no asymptotic freedom);
  - beta_0, beta_1 > 0: beta falls monotonically (QCD-like, no IRFP);
  - beta_0 > 0, beta_1 < 0 at 2, 3, 4 loops: beta dips and re-crosses zero
    at an IR fixed point g_* (dots), the crossing moving with loop order.
Schematic; arbitrary units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator

CGREEN = "#009E73"   # beta_0 < 0
CBLUE = "#0072B2"    # beta_0, beta_1 > 0
CRED = "#D55E00"     # 2 loop
CPINK = "#CC79A7"    # 3 loop
CPURP = "#7B52A1"    # 4 loop

g = np.linspace(0, 1.30, 500)

def beta_fp(g, gstar):
    """Asymptotically free two-loop-like shape with IR zero at gstar."""
    return -g**3 + g**5 / gstar**2

b_green = 0.55 * g**3 + 0.30 * g**2          # beta_0 < 0
b_blue = -(0.55 * g**3 + 0.55 * g**5)        # beta_0, beta_1 > 0
b_2loop = beta_fp(g, 1.02)                   # 2 loop, zero at g_*
b_3loop = beta_fp(g, 0.86)                   # 3 loop
b_4loop = beta_fp(g, 0.72)                   # 4 loop

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ymax, ymin = 0.62, -0.62
for b, c in [(b_green, CGREEN), (b_blue, CBLUE), (b_2loop, CRED),
             (b_3loop, CPINK), (b_4loop, CPURP)]:
    m = (b > ymin) & (b < ymax)
    ax.plot(g[m], b[m], color=c, lw=1.8, zorder=3)

# IR fixed points where the 2-, 3-, 4-loop curves re-cross zero.
for gstar, c in [(1.02, CRED), (0.86, CPINK), (0.72, CPURP)]:
    ax.plot(gstar, 0, "o", ms=5, color=c, zorder=4)
ax.text(1.02, -0.09, r"$g_*$", color=CRED, fontsize=11, ha="center", va="top")
ax.annotate("IR fixed\npoint", xy=(0.79, 0.015), xytext=(0.60, 0.30),
            color=CRED, fontsize=9.5, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=CRED, lw=1.0))

# Direct labels.
ax.text(0.70, 0.54, r"$\beta_0 < 0$", color=CGREEN, fontsize=10, ha="right")
ax.text(0.83, 0.54, "4 loop", color=CPURP, fontsize=10, ha="center")
ax.text(1.02, 0.54, "3 loop", color=CPINK, fontsize=10, ha="center")
ax.text(1.31, 0.38, r"$\beta_0 > 0,\ \beta_1 < 0$" + "\n(2 loop)",
        color=CRED, fontsize=10, ha="right")
ax.text(1.10, -0.56, r"$\beta_0,\ \beta_1 > 0$", color=CBLUE, fontsize=10)

ax.set_xlim(0, 1.34)
ax.set_ylim(ymin, ymax)
ax.set_xlabel(r"$g$")
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
ax.xaxis.set_label_coords(1.0, 0.44)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-041.pdf")
fig.savefig("../fig-redraw-041.png", dpi=200)
print("done")

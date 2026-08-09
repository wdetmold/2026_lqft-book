"""Redraw of fig-notes-028: the Columbia plot.

Chiral/deconfinement transition order in the (m_u = m_d, m_s) plane:
first-order regions (hatched) in the lower-left and upper-right corners,
each bounded by a second-order Z(2) line; second-order O(4) line on the
m_ud = 0 axis above the tricritical point; crossover in between; the
m_u = m_d = m_s diagonal, the physical point, and the pure-gauge corner.
Semantic recreation of the hand-drawn lecture figure; schematic axes.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator
from scipy.interpolate import PchipInterpolator

BLUE = "#0072B2"   # transition lines / hatched 1st-order regions
PURP = "#CC79A7"   # diagonal + physical point
VERM = "#D55E00"   # pure-gauge corner

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")

# ---- lower-left first-order region, bounded by 2nd-order Z(2) line ----
# x(y) through the tricritical point (0, 0.45) and m_crit on the diagonal.
y_lo = np.array([0.00, 0.09, 0.145, 0.20, 0.30, 0.45])
x_lo = np.array([0.18, 0.17, 0.145, 0.115, 0.07, 0.00])
yy = np.linspace(0, 0.45, 200)
xx = PchipInterpolator(y_lo, x_lo)(yy)
ax.plot(xx, yy, color=BLUE, lw=1.6, zorder=4)
ax.fill(np.append(xx, 0.0), np.append(yy, 0.0),
        facecolor="none", edgecolor=BLUE, hatch="///", lw=0, zorder=1)

# ---- upper-right first-order region, bounded by 2nd-order Z(2) line ----
y_hi = np.array([0.60, 0.68, 0.78, 0.86, 1.00])
x_hi = np.array([1.00, 0.86, 0.78, 0.68, 0.60])
yy2 = np.linspace(0.60, 1.00, 200)
xx2 = PchipInterpolator(y_hi, x_hi)(yy2)
ax.plot(xx2, yy2, color=BLUE, lw=1.6, zorder=4)
ax.fill(np.append(xx2, 1.0), np.append(yy2, 1.0),
        facecolor="none", edgecolor=BLUE, hatch="///", lw=0, zorder=1)

# ---- 2nd-order O(4) line on the m_ud = 0 axis, above tricritical point ----
ax.plot([0, 0], [0.45, 1.0], color=BLUE, lw=3.0, zorder=5,
        solid_capstyle="butt")
ax.plot(0, 0.45, "o", color=BLUE, ms=5, zorder=6, clip_on=False)  # tricritical
ax.text(0.035, 0.72, r"$2^{\mathrm{nd}}$ order $O(4)$", color=BLUE,
        rotation=90, ha="left", va="center", fontsize=9)

# ---- diagonal m_u = m_d = m_s ----
ax.plot([0, 1], [0, 1], color=PURP, lw=1.0, zorder=3)

# ---- m_crit on the diagonal ----
ax.plot(0.145, 0.145, "o", color=BLUE, ms=4.5, zorder=6)
ax.text(0.115, 0.205, r"$m^{\mathrm{crit}}$", color=BLUE, fontsize=9,
        ha="left", va="bottom")

# ---- pure-gauge corner ----
ax.plot(1, 1, "o", color=VERM, ms=7, zorder=6, clip_on=False)
ax.text(0.99, 1.05, "pure gauge theory", color=VERM, fontsize=9,
        ha="right", va="bottom")

# ---- physical point ----
ax.plot(0.25, 0.62, "o", mfc="none", mec=PURP, mew=1.5, ms=6, zorder=6)
ax.text(0.29, 0.62, "physical point", color=PURP, fontsize=9,
        ha="left", va="center")

# ---- region / line labels ----
ax.text(0.56, 0.30, "crossover", color="0.3", fontsize=10,
        ha="center", va="center")
ax.annotate(r"$1^{\mathrm{st}}$ order", xy=(0.10, 0.045), xytext=(0.27, 0.03),
            color=BLUE, fontsize=9, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
ax.annotate(r"$2^{\mathrm{nd}}$ order $Z_2$", xy=(0.163, 0.105),
            xytext=(0.33, 0.13), color=BLUE, fontsize=9,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
ax.annotate(r"$1^{\mathrm{st}}$ order", xy=(0.74, 0.925), xytext=(0.40, 0.90),
            color=BLUE, fontsize=9, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
ax.annotate(r"$2^{\mathrm{nd}}$ order $Z_2$", xy=(0.925, 0.645),
            xytext=(0.62, 0.53), color=BLUE, fontsize=9,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))

# ---- schematic axes: square frame, no ticks, 0 and infinity endpoints ----
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_locator(NullLocator())
    axis.set_minor_locator(NullLocator())
ax.text(-0.025, -0.03, r"$0$", ha="right", va="top")
ax.text(1.0, -0.035, r"$\infty$", ha="center", va="top")
ax.text(-0.03, 1.0, r"$\infty$", ha="right", va="center")
ax.text(0.72, -0.035, r"$m_u = m_d$", ha="center", va="top")
ax.text(-0.03, 0.72, r"$m_s$", ha="right", va="center", rotation=90)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-028.pdf")
fig.savefig("../fig-redraw-028.png", dpi=200)
print("done")

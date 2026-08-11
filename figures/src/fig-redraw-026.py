"""Redraw of fig-notes-026: schematic Polyakov-loop susceptibility vs temperature.

Single peaked curve: slow rise from low T, sharp peak at the deconfinement
temperature (~200 MeV in the sketch), long slowly-decaying tail at high T.
Semantic recreation of the hand-drawn lecture figure; arbitrary vertical units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator
from scipy.interpolate import PchipInterpolator

C = "#D55E00"  # vermillion

# Anchor points picked off the sketch (T in MeV, chi in arbitrary units).
anchors_T   = [ 40, 100, 150, 175, 195, 210, 230, 260, 320, 420, 520, 620, 720, 820]
anchors_chi = [0.27, 0.31, 0.40, 0.58, 1.00, 0.70, 0.55, 0.49, 0.44, 0.39, 0.35, 0.32, 0.30, 0.28]

T = np.linspace(40, 820, 600)
chi = PchipInterpolator(anchors_T, anchors_chi)(T)

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(T, chi, color=C, lw=1.8)

ax.set_xlim(40, 840)
ax.set_ylim(0, 1.15)
ax.set_xlabel(r"$T\ \mathrm{[MeV]}$")
ax.set_ylabel(r"$\chi_P$")
ax.set_xticks([200, 400, 600, 800])

# Schematic: no meaningful vertical scale.
ax.set_yticks([])
ax.yaxis.set_minor_locator(NullLocator())

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-026.pdf")
fig.savefig("../fig-redraw-026.png", dpi=200)
print("done")

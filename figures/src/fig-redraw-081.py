"""Redraw of fig-notes-081: axial (U(1)_A / pi--a_1) nondegeneracy measure
chi_A / T^2 versus temperature.

Data points fall monotonically from ~145 MeV toward zero near 200 MeV,
showing restoration of the axial symmetry above T_C. Semantic recreation
of the hand-drawn lecture figure; arbitrary vertical units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator

VERM = "#D55E00"

# Schematic points along a convex decreasing trend, as in the sketch.
T = np.array([148, 156, 164, 172, 181, 190, 198], dtype=float)
chi = 1.3 * np.exp(-(T - 140.0) / 22.0)

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(T, chi, "o", color=VERM, ms=4.5)

ax.set_xlim(140, 205)
ax.set_ylim(0, 1.0)
ax.set_xticks([140, 160, 180, 200])
ax.set_xlabel(r"$T\ \mathrm{[MeV]}$")
ax.set_ylabel(r"$\chi_A / T^2$")

# Schematic: no meaningful vertical scale.
ax.set_yticks([])
ax.yaxis.set_minor_locator(NullLocator())

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-081.pdf")
fig.savefig("../fig-redraw-081.png", dpi=200)
print("done")

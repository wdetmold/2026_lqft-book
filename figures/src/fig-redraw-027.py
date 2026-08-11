"""Redraw of fig-notes-027: schematic chiral-condensate susceptibility vs T.

Two peaked curves of chi_l/T^2 (with schematic lattice "data" points) for two
light-to-strange quark mass ratios: m_l/m_s = 1/40 (higher, sharper peak) and
m_l/m_s = 1/20 (lower, broader peak), both peaking near the chiral crossover
temperature ~157-160 MeV. Semantic recreation of the hand-drawn lecture figure.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator
from scipy.interpolate import PchipInterpolator

C40 = "#CC79A7"  # reddish purple — m_l/m_s = 1/40
C20 = "#0072B2"  # blue           — m_l/m_s = 1/20

# Anchor points picked off the sketch (T in MeV, chi_l/T^2 in arbitrary units).
T40 = [135, 140, 145, 150, 154, 157, 160, 165, 170, 175, 182, 190]
y40 = [0.30, 0.35, 0.45, 0.63, 0.90, 1.00, 0.92, 0.66, 0.52, 0.43, 0.35, 0.29]

T20 = [135, 140, 145, 150, 155, 160, 163, 167, 172, 178, 184, 190]
y20 = [0.27, 0.30, 0.36, 0.46, 0.58, 0.65, 0.63, 0.55, 0.45, 0.36, 0.30, 0.25]

f40 = PchipInterpolator(T40, y40)
f20 = PchipInterpolator(T20, y20)
T = np.linspace(135, 190, 500)

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(T, f40(T), color=C40, lw=1.8, zorder=3)
ax.plot(T, f20(T), color=C20, lw=1.8, zorder=3)

# Schematic lattice data points, as in the sketch.
Tpts = np.array([138, 143, 148, 152, 156, 159, 163, 168, 173, 179, 186])
for f, c in [(f40, C40), (f20, C20)]:
    ax.plot(Tpts, f(Tpts), "o", ms=3.6, mfc="white", mec=c, mew=1.0, ls="none",
            zorder=4)

ax.text(166.5, 0.80, r"$m_l/m_s = 1/40$", color=C40, fontsize=10)
ax.text(172.5, 0.52, r"$m_l/m_s = 1/20$", color=C20, fontsize=10)

ax.set_xlim(133, 192)
ax.set_ylim(0, 1.15)
ax.set_xlabel(r"$T\ \mathrm{[MeV]}$")
ax.set_ylabel(r"$\chi_l/T^2$")
ax.set_xticks([140, 150, 160, 170, 180, 190])

# Schematic: no meaningful vertical scale.
ax.set_yticks([])
ax.yaxis.set_minor_locator(NullLocator())

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-027.pdf")
fig.savefig("../fig-redraw-027.png", dpi=200)
print("done")

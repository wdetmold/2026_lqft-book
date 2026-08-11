"""Redraw of fig-notes-029: schematic chiral condensate M vs T/T_c.

Three decreasing crossover curves (with schematic lattice "data" points) for
m_l/m_s = 1/10, 1/40, 1/80 -- lighter quarks give a lower, steeper curve --
plus the chiral-limit curve (m_l = 0) which vanishes at T/T_c = 1 with
infinite slope. Semantic recreation of the hand-drawn lecture figure;
arbitrary vertical units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator
from scipy.interpolate import PchipInterpolator

C10 = "#0072B2"  # blue           — m_l/m_s = 1/10
C40 = "#D55E00"  # vermillion     — m_l/m_s = 1/40
C80 = "#CC79A7"  # reddish purple — m_l/m_s = 1/80
C0  = "#009E73"  # green          — chiral limit m_l = 0

# Anchor points picked off the sketch (t = T/T_c, M in arbitrary units).
t_anchor = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
M10 = [1.00, 0.99, 0.96, 0.91, 0.83, 0.72, 0.59, 0.48, 0.40]
M40 = [0.92, 0.90, 0.86, 0.78, 0.64, 0.46, 0.30, 0.20, 0.14]
M80 = [0.86, 0.83, 0.77, 0.66, 0.49, 0.29, 0.15, 0.08, 0.05]

f10 = PchipInterpolator(t_anchor, M10)
f40 = PchipInterpolator(t_anchor, M40)
f80 = PchipInterpolator(t_anchor, M80)
t = np.linspace(0, 1.6, 500)

# Chiral limit: second-order-like vanishing at t = 1, M ~ (1 - t^2)^beta.
t0 = np.linspace(0, 1, 400)
M0 = 0.74 * (1.0 - t0**2) ** 0.45

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(t, f10(t), color=C10, lw=1.8, zorder=3)
ax.plot(t, f40(t), color=C40, lw=1.8, zorder=3)
ax.plot(t, f80(t), color=C80, lw=1.8, zorder=3)
ax.plot(t0, M0, color=C0, lw=1.8, zorder=3)

# Schematic lattice data points on the finite-mass curves, as in the sketch.
tpts = np.linspace(0.15, 1.55, 10)
for f, c in [(f10, C10), (f40, C40), (f80, C80)]:
    ax.plot(tpts, f(tpts), "o", ms=3.4, mfc="white", mec=c, mew=1.0, ls="none",
            zorder=4)

ax.text(1.68, 0.40, r"$m_l/m_s = 1/10$", color=C10, fontsize=10, va="center")
ax.text(1.68, 0.14, r"$m_l/m_s = 1/40$", color=C40, fontsize=10, va="center")
ax.text(1.68, 0.05, r"$m_l/m_s = 1/80$", color=C80, fontsize=10, va="center")
ax.text(0.62, 0.28, r"$m_l = 0$", color=C0, fontsize=10, ha="right")

ax.set_xlim(0, 1.65)
ax.set_ylim(0, 1.08)
ax.set_xlabel(r"$T/T_c$")
ax.set_ylabel(r"$M$")
ax.set_xticks([0.0, 0.5, 1.0, 1.5])

# Schematic: no meaningful vertical scale.
ax.set_yticks([])
ax.yaxis.set_minor_locator(NullLocator())

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-029.pdf")
fig.savefig("../fig-redraw-029.png", dpi=200)
print("done")

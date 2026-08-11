"""Redraw of fig-notes-042: walking-technicolour coupling g^2 vs energy scale E.

Solid curve: g^2 diverges towards Lambda_0 in the IR, "walks" (plateaus) at
g_*^2 between Lambda_IR and Lambda_*, then runs down at high energies.
Dashed curve: ordinary QCD-like running for comparison. Red dotted line marks
the plateau value g_*^2. Schematic; arbitrary units.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.ticker import NullLocator

CBLUE = "#0072B2"
CRED = "#D55E00"

L0, LIR, LSTAR = 1.0, 2.0, 6.2   # Lambda_0, Lambda_IR, Lambda_*
GSTAR2 = 0.585                   # plateau value g_*^2

E = np.linspace(1.0, 10.0, 600)
div = 0.08 / (E - 0.75) ** 2.5   # IR divergence towards Lambda_0

# Walking: IR divergence + plateau at g_*^2 + step down beyond Lambda_*.
g2_walk = div + (GSTAR2 - 0.08) * 0.5 * (1 - np.tanh((E - LSTAR) / 0.8)) + 0.08

# QCD-like: same IR divergence, then monotonic decrease (no plateau).
g2_qcd = div + 0.50 * np.exp(-(E - 1.0) / 2.35) + 0.08

fig, ax = plt.subplots(figsize=(4.6, 3.4))

ax.plot(E, g2_walk, color=CBLUE, lw=1.8, zorder=3)
ax.plot(E, g2_qcd, color=CBLUE, lw=1.6, ls="--", zorder=2)

# Plateau marker g_*^2.
ax.plot([0, 2.6], [GSTAR2, GSTAR2], color=CRED, lw=1.2, ls=":", zorder=2)
ax.text(4.0, 0.73, "walking", color=CRED, fontsize=11, ha="center")

ax.set_xlim(0, 10.3)
ax.set_ylim(0, 1.45)
ax.set_xlabel(r"$E$")
ax.set_ylabel(r"$g^2$", rotation=0, labelpad=10)

ax.set_xticks([L0, LIR, LSTAR])
ax.set_xticklabels([r"$\Lambda_0$", r"$\Lambda_{\rm IR}$", r"$\Lambda_*$"])
ax.set_yticks([GSTAR2])
ax.set_yticklabels([r"$g_*^2$"])
ax.tick_params(axis="y", colors=CRED)
for lab in ax.get_yticklabels():
    lab.set_color(CRED)
ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_minor_locator(NullLocator())

# Schematic look: open frame with arrow tips.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(top=False, right=False)
ax.plot(1, 0, ">k", ms=5, transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", ms=5, transform=ax.get_xaxis_transform(), clip_on=False)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-042.pdf")
fig.savefig("../fig-redraw-042.png", dpi=200)
print("done")

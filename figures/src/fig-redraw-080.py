"""Redraw of fig-notes-080: samples of the Polyakov loop P in the complex
plane for N_c = 3.

Symmetric (confined) phase: samples clustered at the origin. Broken
(deconfined) phase: three clusters along the Z_3 center directions
exp(2*pi*i*k/3). Semantic recreation of the hand-drawn lecture figure;
synthetic samples, arbitrary scale.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"   # broken phase
PURP = "#CC79A7"   # symmetric phase

rng = np.random.default_rng(0)

# Symmetric phase: cluster at the origin.
n_sym = 70
sym = rng.normal(0.0, 0.055, n_sym) + 1j * rng.normal(0.0, 0.055, n_sym)

# Broken phase: three Z_3 clusters at radius ~0.75.
n_per = 30
r0 = 0.75
brk = []
for k in range(3):
    center = r0 * np.exp(2j * np.pi * k / 3)
    brk.append(center
               + rng.normal(0.0, 0.05, n_per)
               + 1j * rng.normal(0.0, 0.05, n_per))
brk = np.concatenate(brk)

fig, ax = plt.subplots(figsize=(4.2, 3.6))
ax.set_aspect("equal")

ax.axhline(0, color="0.82", lw=0.7, zorder=0)
ax.axvline(0, color="0.82", lw=0.7, zorder=0)

ax.scatter(brk.real, brk.imag, s=11, color=BLUE, edgecolors="none", zorder=3)
ax.scatter(sym.real, sym.imag, s=11, color=PURP, edgecolors="none", zorder=3)

ax.text(-0.40, 0.87, "broken phase", color=BLUE, fontsize=9,
        ha="center", va="bottom")
ax.text(0.0, -0.28, "symmetric phase", color=PURP, fontsize=9,
        ha="center", va="top")

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_xlabel(r"$\mathrm{Re}\,P$")
ax.set_ylabel(r"$\mathrm{Im}\,P$")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-080.pdf")
fig.savefig("../fig-redraw-080.png", dpi=200)
print("done")

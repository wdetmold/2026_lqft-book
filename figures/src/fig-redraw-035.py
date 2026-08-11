"""Redraw of fig-notes-035 (third panel of fig:int_spec): density of
states rho(E) at the larger lattice size L_2 -- more, more closely spaced
delta functions at the finite-volume energies of fig-redraw-036."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_PURPLE = "#CC79A7"

M_PI = 0.5
L2 = 9.0
YMAX_E = 5.6  # shared energy window with fig-redraw-036
levels = [2.0 * np.sqrt(M_PI**2 + n * (2 * np.pi / L2)**2) for n in range(5)]
levels = [E for E in levels if E <= YMAX_E]

fig, ax = plt.subplots(figsize=(3.4, 2.8))
ax.set_xlim(0, YMAX_E + 0.4)
ax.set_ylim(0, 1.12)
ax.axis("off")

# arrowed axes
ax.annotate("", xy=(YMAX_E + 0.4, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0, 1.12), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            shrinkA=0, shrinkB=0))
ax.text(-0.25, 1.02, r"$\rho(E)$", ha="right", va="center", fontsize=12)
ax.text(YMAX_E + 0.3, -0.1, r"$E$", ha="center", va="top", fontsize=12)

# delta functions at the allowed energies
for E in levels:
    ax.annotate("", xy=(E, 0.78), xytext=(E, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=C_PURPLE, lw=1.6,
                                shrinkA=0, shrinkB=0))

ax.text(0.5 * YMAX_E, 1.05, r"$L_2$", ha="center", va="center",
        color=C_PURPLE, fontsize=12)

fig.savefig("../fig-redraw-035.pdf")
fig.savefig("../fig-redraw-035.png", dpi=200)

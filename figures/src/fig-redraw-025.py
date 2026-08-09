"""Redraw of fig-notes-025: schematic behaviour of the (modulus of the)
Polyakov loop expectation value as a function of temperature.

Near zero in the confined phase, rapid sigmoid rise through the
deconfinement transition, then a slow further increase at high T.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.axis("off")
ax.set_xlim(-70, 740)
ax.set_ylim(-0.28, 1.30)

arrow = dict(arrowstyle="-|>", color="black", lw=0.9,
             shrinkA=0, shrinkB=0, mutation_scale=12)

# ---- axes with arrowheads --------------------------------------------------
ax.annotate("", xy=(0, 1.24), xytext=(0, 0), arrowprops=arrow)
ax.annotate("", xy=(710, 0), xytext=(0, 0), arrowprops=arrow)
ax.text(-25, 1.19, r"$\langle |P| \rangle$", ha="right", va="center",
        fontsize=12)
ax.text(710, -0.10, r"$T\ \mathrm{[MeV]}$", ha="center", va="top",
        fontsize=12)

# ---- x-axis ticks (only 200 and 600 labelled, as in the notes) -------------
for t in [200, 300, 400, 500, 600]:
    ax.plot([t, t], [-0.022, 0.022], color="black", lw=0.9)
for t in [200, 600]:
    ax.text(t, -0.07, rf"${t}$", ha="center", va="top", fontsize=10)

# ---- Polyakov loop: sigmoid rise through deconfinement ---------------------
T = np.linspace(15, 670, 400)
P = PchipInterpolator(
    [15,   80,   150,  200,  230,  260,  290,  330,  400,  500,  600,  670],
    [0.02, 0.025, 0.035, 0.07, 0.20, 0.48, 0.70, 0.82, 0.90, 0.98, 1.05, 1.09])
ax.plot(T, P(T), color=C_BLUE, lw=2.0, zorder=3)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-025.pdf")
fig.savefig("../fig-redraw-025.png", dpi=200)
print("done 025")

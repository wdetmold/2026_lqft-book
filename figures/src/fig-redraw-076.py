"""Redraw of fig-notes-076: the Ginsparg-Wilson circle. Eigenvalues of a
GW operator D lie on the circle |lambda - 1/a| = 1/a in the complex plane
(through the origin, radius 1/a); the doubler modes all sit at
lambda = 2/a."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
ORANGE = "#D55E00"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# axes as arrows through the origin
ax.annotate("", xy=(3.45, 0), xytext=(-1.5, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.annotate("", xy=(0, 1.8), xytext=(0, -1.8),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.text(3.45, -0.16, r"$\mathrm{Re}\,\lambda$", ha="right", va="top",
        fontsize=11)
ax.text(0.12, 1.74, r"$\mathrm{Im}\,\lambda$", ha="left", va="top",
        fontsize=11)

# the GW circle
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(1 + np.cos(th), np.sin(th), color=BLUE, lw=1.8, zorder=3)

# center and radius arrow
ax.plot([1], [0], marker="o", ms=4, color=BLUE, zorder=4)
ax.text(1.02, -0.15, r"$\frac{1}{a}$", color=BLUE, ha="center", va="top",
        fontsize=12)
phi = np.deg2rad(52)
ax.annotate("", xy=(1 + np.cos(phi), np.sin(phi)), xytext=(1, 0),
            arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.3,
                            mutation_scale=11))
ax.text(1 + 0.58 * np.cos(phi) - 0.10, 0.58 * np.sin(phi) + 0.05,
        r"$\frac{1}{a}$", color=BLUE, ha="right", va="bottom", fontsize=12)

# doubler modes at lambda = 2/a
ax.plot([2], [0], marker="o", ms=5, color=ORANGE, zorder=4)
ax.annotate("doubler modes\nall live here",
            xy=(2.04, -0.10), xytext=(2.85, -1.15),
            color=ORANGE, fontsize=10, ha="center", va="top",
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2,
                            connectionstyle="arc3,rad=-0.35",
                            mutation_scale=12))

ax.set_xlim(-1.65, 3.7)
ax.set_ylim(-2.15, 1.95)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-076.pdf")
fig.savefig("../fig-redraw-076.png", dpi=200)
print("done 076")

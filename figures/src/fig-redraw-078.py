"""Redraw of fig-notes-078: a Markov chain (red) containing states (points)
in a state space (green)."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

GREEN = "#009E73"
VERM = "#D55E00"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# State space: smooth irregular blob.
th = np.linspace(0, 2 * np.pi, 400)
r = 1.0 + 0.14 * np.sin(2 * th + 1.1) + 0.10 * np.cos(3 * th + 0.4)
bx = 1.55 * r * np.cos(th)
by = 1.10 * r * np.sin(th)
ax.fill(bx, by, facecolor=GREEN, alpha=0.15, edgecolor=GREEN, lw=1.8, zorder=1)

# Markov chain: sequence of states connected by transitions.
pts = np.array([
    (-0.55, 0.72),
    (0.15, 0.55),
    (-0.95, 0.28),   # s
    (0.95, 0.38),    # s'
    (-0.25, -0.02),
    (-1.05, -0.18),
    (-0.60, -0.58),
    (-0.02, -0.42),
    (0.35, -0.66),
    (0.62, -0.28),
    (1.00, -0.55),
])

for p, q in zip(pts[:-1], pts[1:]):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.3,
                                mutation_scale=13, shrinkA=3, shrinkB=3),
                zorder=3)
ax.scatter(pts[:, 0], pts[:, 1], s=26, color=VERM, zorder=4)

ax.text(-1.08, 0.38, r"$s$", fontsize=12, ha="right", va="bottom", color="k")
ax.text(1.08, 0.44, r"$s'$", fontsize=12, ha="left", va="bottom", color="k")

ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-1.55, 1.55)

fig.savefig("../fig-redraw-078.pdf")
fig.savefig("../fig-redraw-078.png", dpi=200)
print("done 078")

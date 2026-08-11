"""Redraw of fig-notes-009: one possible path z_mu(s) from x_mu = z_mu(0) to
y = z_mu(t), with the tangent vector n_mu(s) at an intermediate point (used
for parallel transporters).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_RED = "#D55E00"
C_GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.axis("off")

# ---- coordinate axes -------------------------------------------------------
ax.annotate("", xy=(1.02, 0), xytext=(-0.02, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.annotate("", xy=(0, 1.00), xytext=(0, -0.02),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))

# ---- the path z_mu(s) ------------------------------------------------------
px = np.array([0.22, 0.32, 0.44, 0.55, 0.63, 0.70])
py = np.array([0.22, 0.32, 0.395, 0.50, 0.67, 0.88])
f = PchipInterpolator(px, py)
x = np.linspace(px[0], px[-1], 300)
ax.plot(x, f(x), color=C_RED, lw=1.8, zorder=3)

# endpoints
ax.plot([px[0]], [py[0]], marker="o", ms=6, color=C_RED, zorder=4)
ax.plot([px[-1]], [py[-1]], marker="o", ms=6, color=C_RED, zorder=4)
ax.text(0.22, 0.155, r"$x_\mu = z_\mu(0)$", color=C_RED, ha="center",
        va="top", fontsize=11)
ax.text(0.735, 0.895, r"$y = z_\mu(t)$", color=C_RED, ha="left",
        va="center", fontsize=11)

# path label
ax.annotate(r"path $z_\mu(s)$", xy=(0.475, 0.425), xytext=(0.80, 0.33),
            color=C_RED, ha="left", va="center", fontsize=11,
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=0.9,
                            shrinkA=4, shrinkB=3))

# ---- tangent vector at an intermediate point z_mu(s) -----------------------
s = 0.55
ts = np.array([1.0, float(f.derivative()(s))])
ts /= np.hypot(*ts)
p0 = np.array([s, float(f(s))])
tip = p0 + 0.30 * ts
ax.annotate("", xy=tuple(tip), xytext=tuple(p0),
            arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=1.6,
                            mutation_scale=12), zorder=4)
ax.annotate(r"tangent vector $n_\mu(s)$", xy=tuple(p0 + 0.20 * ts),
            xytext=(0.28, 0.78), color=C_GREEN, ha="center", va="center",
            fontsize=10,
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=0.9,
                            connectionstyle="arc3,rad=0.3",
                            shrinkA=4, shrinkB=5))

ax.set_xlim(-0.06, 1.06)
ax.set_ylim(-0.06, 1.02)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-009.pdf")
fig.savefig("../fig-redraw-009.png", dpi=200)
print("done 009")

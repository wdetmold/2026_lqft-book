"""Redraw of fig-notes-057: final beta function of the O(n) model.

beta_CS(g_R) rises monotonically from the trivial IR fixed point at g_R = 0
and does not turn over even non-perturbatively (out to g_R ~ 40); so for any
non-zero renormalized coupling there is no continuum limit.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.axis("off")

# ---- axes ------------------------------------------------------------------
ax.annotate("", xy=(53, 0), xytext=(-1.5, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.annotate("", xy=(0, 0.98), xytext=(0, -0.02),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.text(54.5, 0, r"$g_R$", ha="left", va="center", fontsize=11)
ax.text(1.8, 0.96, r"$\beta_{CS}(g_R)$", ha="left", va="top", fontsize=11)

# tick at g_R ~ 40
ax.plot([40, 40], [-0.018, 0.018], color="black", lw=0.9)
ax.text(40, -0.055, r"$\sim 40$", ha="center", va="top", fontsize=10)

# ---- beta function: monotonic, never turns over ----------------------------
g = np.linspace(0, 46, 300)
beta = 0.82 * (g / 46) ** 2.2
ax.plot(g, beta, color=C_BLUE, lw=1.8, zorder=3)

# trivial IR fixed point at the origin
ax.plot([0], [0], marker="o", ms=7, color=C_RED, zorder=5, clip_on=False)
ax.annotate("trivial IR fixed point", xy=(0.9, -0.015), xytext=(3.5, -0.14),
            color=C_RED, ha="left", va="center", fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=0.9,
                            connectionstyle="arc3,rad=0.25",
                            shrinkA=2, shrinkB=3))

# IR flow arrows towards the fixed point
for g1, g0 in [(26, 18.5), (16, 8.5)]:
    y1 = 0.82 * (g1 / 46) ** 2.2 + 0.045
    y0 = 0.82 * (g0 / 46) ** 2.2 + 0.045
    ax.annotate("", xy=(g0, y0), xytext=(g1, y1),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.5,
                                mutation_scale=12), zorder=4)

# ---- annotations -----------------------------------------------------------
ax.text(34.0, 0.29, "does not turn over even\nnon-perturbatively",
        color=C_BLUE, ha="left", va="center", fontsize=9)
ax.text(34.0, 0.10, "compelling numerical\nevidence, but not a proof",
        color=C_RED, ha="left", va="center", fontsize=9)

ax.set_xlim(-3, 58)
ax.set_ylim(-0.20, 1.0)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-057.pdf")
fig.savefig("../fig-redraw-057.png", dpi=200)
print("done 057")

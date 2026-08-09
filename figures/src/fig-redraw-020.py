"""Redraw of fig-notes-020: finite fifth dimension -s0 < s < s0 with
periodic boundary conditions. M(s) = m sgn(s) (red) has a kink at s = 0
and one of opposite discontinuity at s = +/- s0 (periodic images dashed);
zero modes b0, bound to s = 0 (solid blue), and f0, bound to s = +/- s0
(dashed blue)."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

RED = "#D55E00"
BLUE = "#0072B2"

m, s0, A = 1.0, 3.0, 1.7
s = np.linspace(-s0, s0, 600)

fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.axis("off")

# axes: s axis as an arrow, vertical guide at s = 0
ax.annotate("", xy=(4.35, 0), xytext=(-4.25, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.plot([0, 0], [-1.5, 2.15], color="0.65", lw=0.8, zorder=1)
ax.text(4.4, -0.12, r"$s$", fontsize=12, ha="left", va="top")
for x, lab, ha in [(-s0, r"$-s_0$", "right"), (s0, r"$s_0$", "left")]:
    ax.plot([x, x], [-0.08, 0.08], color="black", lw=0.9, zorder=2)
    ax.text(x + (0.18 if ha == "left" else -0.18), -0.42, lab,
            ha=ha, va="top", fontsize=11)

# M(s) = m sgn(s) on -s0 < s < s0, with periodic images dashed
ax.plot([-s0, 0], [-m, -m], color=RED, lw=2.2, solid_capstyle="round",
        zorder=3)
ax.plot([0, 0], [-m, m], color=RED, lw=2.2, zorder=3)
ax.plot([0, s0], [m, m], color=RED, lw=2.2, solid_capstyle="round", zorder=3)
dsh = dict(color=RED, lw=1.8, ls=(0, (3.5, 2.5)), zorder=3)
ax.plot([s0, s0], [m, -m], **dsh)          # opposite kink at s = s0
ax.plot([-s0, -s0], [m, -m], **dsh)        # its periodic image at -s0
ax.plot([s0, s0 + 0.8], [-m, -m], **dsh)   # periodic continuation
ax.plot([-s0 - 0.8, -s0], [m, m], **dsh)
ax.text(1.55, m + 0.14, r"$M(s)$", color=RED, fontsize=12,
        ha="center", va="bottom")

# zero modes: b0 bound to s = 0, f0 bound to s = +/- s0
ax.plot(s, A * np.exp(-m * np.abs(s)), color=BLUE, lw=2.0, zorder=4)
ax.plot(s, A * np.exp(-m * (s0 - np.abs(s))), color=BLUE, lw=2.0,
        ls=(0, (4, 2.5)), zorder=4)
ax.text(0.18, A + 0.10, r"$b_0$", color=BLUE, fontsize=12,
        ha="left", va="bottom")
ax.text(2.42, 1.32, r"$f_0$", color=BLUE, fontsize=12,
        ha="right", va="bottom")

ax.set_xlim(-4.9, 5.0)
ax.set_ylim(-1.75, 2.35)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-020.pdf")
fig.savefig("../fig-redraw-020.png", dpi=200)
print("done 020")

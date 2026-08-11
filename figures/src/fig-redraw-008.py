"""Redraw of fig-notes-008: schematic curves of constant lambda_R in the
(lambda_0, kappa/kappa_c) plane.

Curves of constant lambda_R > 0 approach the critical line kappa/kappa_c = 1
but terminate at lambda_0 = infinity at a value != 1; only the lambda_R = 0
curve (hugging lambda_0 = 0) reaches the critical line, so only it admits a
continuum limit.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_RED = "#D55E00"
C_GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("auto")
ax.axis("off")


def curve(ax, pts, arrow_fracs, color=C_GREEN):
    pts = np.asarray(pts, float)
    x = np.linspace(pts[0, 0], pts[-1, 0], 240)
    y = PchipInterpolator(pts[:, 0], pts[:, 1])(x)
    ax.plot(x, y, color=color, lw=1.5, zorder=2)
    for f in arrow_fracs:
        i = int(f * (len(x) - 4))
        ax.annotate("", xy=(x[i + 3], y[i + 3]), xytext=(x[i], y[i]),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5,
                                    mutation_scale=11), zorder=3)


# ---- axes drawn by hand ----------------------------------------------------
# vertical axis
ax.plot([0, 0], [0, 1.45], color="black", lw=0.9, zorder=1)
ax.text(0.03, 1.44, r"$\kappa/\kappa_c(\lambda)$", ha="left", va="top",
        fontsize=11)
# horizontal line at kappa/kappa_c = 1 (arrowed, labelled lambda_0)
ax.annotate("", xy=(1.10, 1.0), xytext=(0, 1.0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12), zorder=1)
ax.text(1.125, 1.0, r"$\lambda_0$", ha="left", va="center", fontsize=11)
# tick '1' where the line meets the vertical axis
ax.plot([-0.012, 0.012], [1.0, 1.0], color="black", lw=0.9)
ax.text(-0.03, 1.0, "1", ha="right", va="center", fontsize=10)

# ---- lambda_R = 0 curve: hugs lambda_0 = 0, reaches the critical line ------
ax.plot([0.02, 0.02], [0.10, 0.998], color=C_GREEN, lw=1.5, zorder=2)
ax.text(0.05, 0.06, r"$\lambda_R = 0$", color=C_GREEN, ha="left",
        va="center", fontsize=10)

# ---- constant lambda_R > 0 curves below the critical line ------------------
curve(ax, [(0.055, 0.10), (0.085, 0.55), (0.14, 0.82), (0.30, 0.905),
           (0.60, 0.925), (1.00, 0.930)], [0.10, 0.45])
curve(ax, [(0.13, 0.10), (0.20, 0.48), (0.32, 0.72), (0.55, 0.83),
           (1.00, 0.870)], [0.15, 0.55])
curve(ax, [(0.34, 0.10), (0.48, 0.42), (0.66, 0.62), (1.00, 0.755)],
      [0.30, 0.70])

# ---- constant lambda_R curves above the critical line ----------------------
curve(ax, [(0.03, 1.42), (0.12, 1.20), (0.30, 1.085), (0.60, 1.035),
           (1.00, 1.020)], [0.25, 0.65])
curve(ax, [(0.17, 1.45), (0.30, 1.27), (0.50, 1.145), (0.75, 1.085),
           (1.00, 1.065)], [0.30, 0.70])
curve(ax, [(0.42, 1.45), (0.58, 1.30), (0.78, 1.195), (1.00, 1.150)],
      [0.35, 0.75])

# ---- red bracket: at lambda_0 = infinity the curves end at != 1 ------------
bx = 1.035
ax.plot([bx, bx + 0.015, bx + 0.015, bx], [0.988, 0.988, 0.935, 0.935],
        color=C_RED, lw=1.2, zorder=3)
ax.text(bx + 0.035, 0.955, r"$\neq 1$", color=C_RED, ha="left",
        va="center", fontsize=11)

ax.set_xlim(-0.12, 1.30)
ax.set_ylim(0, 1.50)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-008.pdf")
fig.savefig("../fig-redraw-008.png", dpi=200)
print("done 008")

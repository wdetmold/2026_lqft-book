import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of fig-notes-091.pdf (flow1): hypothetical beta_CS(g_R) with three
# zeros g_1 (IR), g_2 (UV), g_3 (IR). Red arrows indicate the flow as
# Lambda ~ 1/(m_R a) -> infinity (i.e. towards the continuum limit).

import numpy as np
from scipy.interpolate import PchipInterpolator

C_CURVE = "#009E73"   # beta function (green in the notes)
C_FLOW = "#D55E00"    # flow arrows / annotation (red in the notes)

g1, g2, g3 = 0.15, 0.48, 0.85

fig, ax = plt.subplots(figsize=(5.4, 3.1))
ax.axis("off")

beta = PchipInterpolator(
    [-0.05, g1, 0.31, g2, 0.67, g3, 1.00],
    [-0.35, 0.0, 0.22, 0.0, -0.22, 0.0, 0.45])
x = np.linspace(-0.05, 1.0, 400)
ax.plot(x, beta(x), color=C_CURVE, lw=1.7, zorder=3)

# axes as arrows
ax.annotate("", xy=(1.13, 0.0), xytext=(-0.10, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.annotate("", xy=(0.0, 0.56), xytext=(0.0, -0.48),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.text(-0.015, 0.55, r"$\beta_{CS}(g_R)$", ha="right", va="center",
        fontsize=11)
ax.text(1.13, -0.055, "$g_R$", ha="center", va="top", fontsize=11)

# fixed points: ticks, labels, and IR/UV markers
for g, lab in [(g1, "$g_1$"), (g2, "$g_2$"), (g3, "$g_3$")]:
    ax.plot([g, g], [-0.018, 0.018], color=C_CURVE, lw=1.4, zorder=4)
    ax.text(g, -0.055, lab, color=C_CURVE, ha="center", va="top",
            fontsize=11)
ax.text(g1 + 0.055, -0.045, "IR", ha="left", va="top", fontsize=10)
ax.text(g2, 0.055, "UV", ha="center", va="bottom", fontsize=10)
ax.text(g3, 0.055, "IR", ha="center", va="bottom", fontsize=10)

# flow arrows (towards g_1 and g_3, away from g_2)
arrow = dict(arrowstyle="-|>", color=C_FLOW, lw=1.5, shrinkA=0, shrinkB=0)
ax.annotate("", xy=(0.105, -0.075), xytext=(0.035, -0.185),
            arrowprops=arrow)                       # up towards g_1
ax.annotate("", xy=(0.235, 0.285), xytext=(0.335, 0.285),
            arrowprops=arrow)                       # left towards g_1
ax.annotate("", xy=(0.735, -0.29), xytext=(0.615, -0.29),
            arrowprops=arrow)                       # right towards g_3
ax.annotate("", xy=(0.905, 0.245), xytext=(0.975, 0.375),
            arrowprops=arrow)                       # down towards g_3

# legend for the arrows
ax.annotate("", xy=(0.30, 0.60), xytext=(0.24, 0.60), arrowprops=arrow)
ax.text(0.325, 0.60,
        r"indicates flow as $\Lambda\sim 1/(m_R a)\rightarrow\infty$"
        "\n(i.e. continuum limit)",
        color=C_FLOW, ha="left", va="center", fontsize=9.5)

ax.set_xlim(-0.14, 1.16)
ax.set_ylim(-0.52, 0.70)

fig.savefig("../fig-redraw-091.pdf")
fig.savefig("../fig-redraw-091.png", dpi=200)

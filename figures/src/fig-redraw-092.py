import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of fig-notes-092.pdf (flow2): flow in the bare parameters
# (g_0, m_0 a) for the fixed-point structure of fig-notes-091. Green curves
# of fixed g_R flow upwards towards the m_R a = 0 line (continuum limit);
# curves with g_1 <= g_R <= g_3 reach it (bare coupling driven to the UV
# fixed point g_2), the curve outside that range escapes.

import numpy as np
from scipy.interpolate import PchipInterpolator

C_CRIT = "#D55E00"    # m_R a = 0 line (red in the notes)
C_FLOW = "#009E73"    # curves of fixed g_R (green in the notes)

g1, g2, g3 = 0.30, 0.55, 0.80

fig, ax = plt.subplots(figsize=(5.4, 3.3))
ax.axis("off")

# axes as arrows
ax.annotate("", xy=(1.10, 0.0), xytext=(-0.045, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.annotate("", xy=(0.0, 1.02), xytext=(0.0, -0.09),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.text(-0.02, 1.00, "$m_0 a$", ha="right", va="center", fontsize=11)
ax.text(1.10, -0.045, "$g_0$", ha="center", va="top", fontsize=11)

# m_R a = 0 line (continuum limit)
xs = np.linspace(0.0, 0.96, 200)
crit = PchipInterpolator([0.00, 0.30, 0.55, 0.80, 0.96],
                         [0.70, 0.755, 0.81, 0.84, 0.85])
ax.plot(xs, crit(xs), color=C_CRIT, lw=1.8, zorder=4)
for g in (g1, g2, g3):
    ax.plot(g, crit(g), "o", color=C_CRIT, ms=4.5, zorder=5)
ax.text(0.99, 0.855, "$m_R a = 0$\ncontinuum limit", color=C_CRIT,
        ha="left", va="center", fontsize=9.5)


def flow(pts, arrow_at=0.5, end_arrow=False):
    """Draw one curve of fixed g_R through pts with an upward arrowhead."""
    pts = np.asarray(pts, dtype=float)
    t = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
    t /= t[-1]
    fx = PchipInterpolator(t, pts[:, 0])
    fy = PchipInterpolator(t, pts[:, 1])
    s = np.linspace(0, 1, 200)
    ax.plot(fx(s), fy(s), color=C_FLOW, lw=1.5, zorder=3)
    a = 1.0 if end_arrow else arrow_at
    ax.annotate("", xy=(fx(a), fy(a)), xytext=(fx(a - 0.04), fy(a - 0.04)),
                arrowprops=dict(arrowstyle="-|>", color=C_FLOW, lw=1.5,
                                shrinkA=0, shrinkB=0))


# curves of fixed g_R
flow([(0.04, 0.58), (0.12, 0.44), (0.19, 0.40), (0.25, 0.50),
      (0.283, 0.72)], arrow_at=0.85)          # g_R < g_1: rises left of g_1
flow([(g1, 0.03), (g1, crit(g1))])            # g_R = g_1 fixed point
flow([(0.335, 0.03), (0.355, 0.45), (0.46, 0.72), (0.535, 0.795)])
flow([(0.445, 0.03), (0.465, 0.45), (0.52, 0.73), (0.542, 0.795)])
flow([(g2, 0.03), (g2, crit(g2))])            # g_R = g_2 fixed point
flow([(0.655, 0.03), (0.635, 0.45), (0.585, 0.75), (0.558, 0.795)])
flow([(0.765, 0.03), (0.735, 0.45), (0.635, 0.755), (0.568, 0.80)])
flow([(g3, 0.03), (g3, crit(g3))])            # g_R = g_3 fixed point
flow([(0.875, 0.03), (0.92, 0.32), (1.00, 0.56)], end_arrow=True)
# g_R > g_3: escapes

# fixed-point markers below the axis
for g, lab in [(g1, "$g_1$"), (g2, "$g_2$"), (g3, "$g_3$")]:
    ax.annotate("", xy=(g, -0.02), xytext=(g, -0.11),
                arrowprops=dict(arrowstyle="-|>", color=C_FLOW, lw=1.2,
                                shrinkA=0, shrinkB=0))
    ax.text(g, -0.13, lab, color=C_FLOW, ha="center", va="top", fontsize=11)

ax.text(0.99, 0.42, "curves of\nfixed $g_R$", color=C_FLOW, ha="left",
        va="center", fontsize=9.5)

ax.set_xlim(-0.07, 1.32)
ax.set_ylim(-0.24, 1.06)

fig.savefig("../fig-redraw-092.pdf")
fig.savefig("../fig-redraw-092.png", dpi=200)

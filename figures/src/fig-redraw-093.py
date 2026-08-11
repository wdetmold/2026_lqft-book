import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of the figural content of fig-notes-093.pdf (handwritten notes page):
# the discretised-path sketch. A path x(t) between x_0 and x_N sampled on the
# time slices t_0 ... t_N (x(j eps) = x_j), drawn in the (t, x) plane.
# The equations on the notes page are already transcribed in the tex.

import numpy as np

C_PATH = "#D55E00"    # the path (red in the notes)
C_SLICE = "#009E73"   # time-slice lines (green in the notes)

fig, ax = plt.subplots(figsize=(5.4, 3.1))
ax.axis("off")

N = 9
tj = np.arange(N + 1, dtype=float)
xj = np.array([0.38, 0.27, 0.44, 0.62, 0.80, 0.66, 0.73, 0.44, 0.27, 0.33])

# time-slice lines
for t in tj:
    ax.plot([t, t], [0.0, 0.92], color=C_SLICE, lw=1.0, alpha=0.75, zorder=1)

# axes as arrows
ax.annotate("", xy=(10.4, 0.0), xytext=(-0.7, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.annotate("", xy=(-0.35, 1.02), xytext=(-0.35, -0.10),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.text(-0.55, 1.00, "$x$", ha="right", va="center", fontsize=11)
ax.text(10.55, -0.02, "$t$", ha="left", va="center", fontsize=11)

# the discretised path
ax.plot(tj, xj, color=C_PATH, lw=1.6, zorder=3)
ax.plot(tj, xj, "o", color=C_PATH, ms=3.4, zorder=4)

# point labels
ax.text(tj[0] - 0.18, xj[0] + 0.02, "$x_0$", color=C_PATH, ha="right",
        va="center", fontsize=10)
ax.text(tj[1] + 0.10, xj[1] - 0.09, "$x_1$", color=C_PATH, ha="left",
        va="center", fontsize=10)
ax.text(tj[-1] + 0.12, xj[-1] + 0.07, "$x_N$", color=C_PATH, ha="left",
        va="center", fontsize=10)

# annotation naming the path
ax.annotate("path$\\;=\\;\\{x_0=x(t_0),\\,x_1,\\,\\ldots,\\,x_N\\}$",
            xy=(5.5, 0.70), xytext=(5.1, 1.06), color=C_PATH, fontsize=10,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C_PATH, lw=0.9,
                            connectionstyle="arc3,rad=0.25",
                            shrinkA=2, shrinkB=3))

# time labels below the axis
for t, lab in [(0, "$t_0$"), (1, "$t_1$"), (N - 1, "$t_{N-1}$"), (N, "$t_N$")]:
    ax.text(t, -0.09, lab, ha="center", va="top", fontsize=10)
ax.text(4.5, -0.09, r"$\cdots$", ha="center", va="top", fontsize=10)

ax.set_xlim(-1.2, 11.2)
ax.set_ylim(-0.28, 1.14)

fig.savefig("../fig-redraw-093.pdf")
fig.savefig("../fig-redraw-093.png", dpi=200)

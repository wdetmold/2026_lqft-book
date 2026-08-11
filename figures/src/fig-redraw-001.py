import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of fig-notes-001.jpg: contour in the complex z-plane for the p_4
# integral. Unit-circle contour (counterclockwise) enclosing the pole z_-
# but not z_+, both on the positive real axis.

import numpy as np

C_CONT = "#0072B2"   # contour
C_POLE = "#D55E00"   # poles

fig, ax = plt.subplots(figsize=(2.9, 2.7))
ax.axis("off")
ax.set_aspect("equal")

# axes as arrows through the origin
ax.annotate("", xy=(1.62, 0.0), xytext=(-1.45, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9))
ax.annotate("", xy=(0.0, 1.55), xytext=(0.0, -1.45),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9))

# unit-circle contour, counterclockwise
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color=C_CONT, lw=1.5, zorder=3)
a0, a1 = np.deg2rad(58), np.deg2rad(72)
ax.annotate("", xy=(np.cos(a1), np.sin(a1)), xytext=(np.cos(a0), np.sin(a0)),
            arrowprops=dict(arrowstyle="-|>", color=C_CONT, lw=1.4,
                            shrinkA=0, shrinkB=0))

# poles: z_- inside, z_+ outside the contour
ax.plot([0.60], [0.0], "o", color=C_POLE, ms=4.5, zorder=4)
ax.plot([1.30], [0.0], "o", color=C_POLE, ms=4.5, zorder=4)
# NB: mathtext in this environment drops a trailing lone subscript minus
# ("$z_-$" renders as "z"), so the minus is drawn as a plain-text glyph.
ax.text(0.55, -0.18, "$z$", color=C_POLE, ha="center", va="top",
        fontsize=13)
ax.text(0.69, -0.33, "−", color=C_POLE, ha="center", va="top",
        fontsize=8.5)
ax.text(1.33, -0.18, "$z_{\\,+}$", color=C_POLE, ha="center", va="top",
        fontsize=13)

# complex-plane marker in the upper right corner
ax.plot([1.28, 1.28, 1.62], [1.18, 1.46, 1.46], color="k", lw=0.9)
ax.text(1.36, 1.28, "$z$", ha="left", va="center", fontsize=12)

ax.set_xlim(-1.55, 1.75)
ax.set_ylim(-1.55, 1.65)

fig.savefig("../fig-redraw-001.pdf")
fig.savefig("../fig-redraw-001.png", dpi=200)

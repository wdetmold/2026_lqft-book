"""Redraw of fig-notes-047: the Schroedinger-functional geometry used to
define the coupling -- a space-time cylinder with fixed boundaries at t=0 and
t=L (periodic spatial directions, volume L^3) supporting a background
chromo-electric field E."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import Ellipse

BLUE = "#0072B2"
LBLUE = "#dbe9f6"
LPINK = "#f4e6f2"
ORANGE = "#D55E00"

W, H = 2.4, 2.6
RY = 0.42

fig, ax = plt.subplots(figsize=(4.4, 2.8))
ax.set_aspect("equal")
ax.axis("off")

cx = 0.0
# walls
for s in (-1, 1):
    ax.plot([cx + s * W / 2, cx + s * W / 2], [0, H], color=BLUE, lw=1.7,
            zorder=2)
# caps: fixed boundary fields at t=0 and t=L
ax.add_patch(Ellipse((cx, 0), W, RY, facecolor=LBLUE, edgecolor=BLUE,
                     lw=1.7, zorder=3))
ax.add_patch(Ellipse((cx, H), W, RY, facecolor=LPINK, edgecolor=BLUE,
                     lw=1.7, zorder=3))

# background chromo-electric field: curved arrow inside the cylinder
ym = 0.52 * H
ax.annotate("",
            xy=(cx - 0.40 * W, ym + 0.04),
            xytext=(cx + 0.34 * W, ym - 0.06),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.8,
                            mutation_scale=14,
                            connectionstyle="arc3,rad=0.28"))
ax.text(cx + 0.02, ym + 0.42, r"$\vec{E}$", ha="center", va="center",
        fontsize=15, color=ORANGE)

# annotations on the right
ax.text(W / 2 + 0.35, H + 0.16, r"$t = L$", ha="left", va="center",
        fontsize=13)
ax.text(W / 2 + 0.35, -0.16, r"$t = 0$", ha="left", va="center",
        fontsize=13)
ax.text(W / 2 + 0.35, 0.52 * H, "periodic spatial\ndirections $L^3$",
        ha="left", va="center", fontsize=11)

ax.set_xlim(-W / 2 - 0.4, W / 2 + 2.6)
ax.set_ylim(-0.55, H + 0.55)

fig.savefig("../fig-redraw-047.pdf")
fig.savefig("../fig-redraw-047.png", dpi=200)

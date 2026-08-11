"""Redraw of fig-notes-074: an example of the action of the coboundary
operator on a 1-chain (an oriented link):

    Nabla(x, {mu}) = (x - nu_hat, {mu,nu}) - (x, {mu,nu}),

drawn as Nabla(link) = the two plaquettes sharing the link, with opposite
signs (shown for the sign function rho = +1).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import Rectangle

GREEN = "#009E73"
BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 2.2))
ax.set_aspect("equal")
ax.axis("off")

# Nabla ( link ) =
ax.text(-0.15, 0.0, r"$\nabla$", fontsize=14, ha="center", va="center")
ax.text(0.22, -0.02, "(", fontsize=26, ha="center", va="center")
ax.text(1.78, -0.02, ")", fontsize=26, ha="center", va="center")

x0, x1 = 0.5, 1.5
ax.plot([x0, x1], [0, 0], color=GREEN, lw=1.6, zorder=2)
ax.annotate("", xy=(0.5 * (x0 + x1) + 0.13, 0), xytext=(0.5 * (x0 + x1) - 0.13, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6,
                            mutation_scale=14), zorder=3)

ax.text(2.2, 0.0, "=", fontsize=13, ha="center", va="center")

# The two plaquettes sharing the link, with opposite signs.
px = 2.85  # left edge of the plaquettes
w = 1.0
ax.add_patch(Rectangle((px, 0), w, w, facecolor=GREEN, alpha=0.15,
                       edgecolor=GREEN, lw=1.2, zorder=2))
ax.add_patch(Rectangle((px, -w), w, w, facecolor=GREEN, alpha=0.15,
                       edgecolor=GREEN, lw=1.2, zorder=2))

# The original link, shared by both plaquettes.
ax.plot([px, px + w], [0, 0], color=GREEN, lw=1.8, zorder=3)
ax.annotate("", xy=(px + 0.5 * w + 0.13, 0), xytext=(px + 0.5 * w - 0.13, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8,
                            mutation_scale=14), zorder=4)

ax.text(px + 0.5 * w, -0.5 * w, r"$+$", fontsize=12, ha="center", va="center")
ax.text(px + 0.5 * w, 0.5 * w, r"$-$", fontsize=12, ha="center", va="center")

# Term labels.
ax.text(px + w + 0.15, -0.5 * w, r"$(x-\hat{\nu},\{\mu,\nu\})$",
        fontsize=9.5, ha="left", va="center")
ax.text(px + w + 0.15, 0.5 * w, r"$(x,\{\mu,\nu\})$",
        fontsize=9.5, ha="left", va="center")

ax.set_xlim(-0.5, 5.6)
ax.set_ylim(-1.35, 1.35)

fig.savefig("../fig-redraw-074.pdf")
fig.savefig("../fig-redraw-074.png", dpi=200)
print("done 074")

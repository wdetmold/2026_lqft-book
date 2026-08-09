"""Redraw of fig-notes-073: an example of the action of the boundary
operator on a 1-chain (an oriented link):

    Delta(x, {mu}) = (x + mu_hat, {}) - (x, {}),

drawn as Delta(link) = signed pair of endpoint sites.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

GREEN = "#009E73"
BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 1.5))
ax.set_aspect("equal")
ax.axis("off")

# Delta ( link ) =
ax.text(-0.15, 0.0, r"$\Delta$", fontsize=14, ha="center", va="center")
ax.text(0.22, -0.02, "(", fontsize=26, ha="center", va="center")
ax.text(1.98, -0.02, ")", fontsize=26, ha="center", va="center")

# The oriented link x -> x + mu_hat.
x0, x1 = 0.55, 1.65
ax.plot([x0, x1], [0, 0], color=GREEN, lw=1.6, zorder=2)
ax.annotate("", xy=(0.5 * (x0 + x1) + 0.13, 0), xytext=(0.5 * (x0 + x1) - 0.13, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6,
                            mutation_scale=14), zorder=3)
ax.scatter([x0, x1], [0, 0], s=42, color=BLUE, zorder=4)
ax.text(x0, -0.30, r"$x$", fontsize=10, ha="center", va="top")
ax.text(x1, -0.30, r"$x+\hat{\mu}$", fontsize=10, ha="center", va="top")

ax.text(2.45, 0.0, "=", fontsize=13, ha="center", va="center")

# Boundary: (x + mu_hat) - (x), shown as signed endpoint sites.
xa, xb = 3.1, 4.2
ax.scatter([xa, xb], [0, 0], s=42, color=BLUE, zorder=4)
ax.text(xa, 0.22, r"$-$", fontsize=11, ha="center", va="bottom")
ax.text(xb, 0.22, r"$+$", fontsize=11, ha="center", va="bottom")
ax.text(xa, -0.30, r"$x$", fontsize=10, ha="center", va="top")
ax.text(xb, -0.30, r"$x+\hat{\mu}$", fontsize=10, ha="center", va="top")

ax.set_xlim(-0.5, 4.8)
ax.set_ylim(-0.75, 0.75)

fig.savefig("../fig-redraw-073.pdf")
fig.savefig("../fig-redraw-073.png", dpi=200)
print("done 073")

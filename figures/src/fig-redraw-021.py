"""Redraw of fig-notes-021: schematic of one leapfrog integration step.
Step a: P takes a half-step to epsilon/2; step b: Q leapfrogs from 0 to
epsilon using P(epsilon/2); step c: P steps from epsilon/2 to epsilon."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

VERM = "#D55E00"
BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 2.4))
ax.set_aspect("equal")
ax.axis("off")

# Time line with the three points 0, eps/2, eps.
ax.plot([-0.35, 2.35], [0, 0], color="0.75", lw=0.8, zorder=1)
ax.scatter([0, 1, 2], [0, 0, 0], s=55, color=BLUE, zorder=4)
for x, s in [(0, r"$0$"), (1, r"$\varepsilon/2$"), (2, r"$\varepsilon$")]:
    ax.text(x, -0.20, s, fontsize=11, ha="center", va="top")

arc = dict(color=VERM, lw=1.5, mutation_scale=15, shrinkA=5, shrinkB=5)

# a: P half-step 0 -> eps/2 (above).
ax.annotate("", xy=(1, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3,rad=-0.55", **arc), zorder=3)
ax.text(0.5, 0.50, r"$a$", fontsize=12, ha="center", va="bottom", color=VERM)

# c: P step eps/2 -> eps (above).
ax.annotate("", xy=(2, 0), xytext=(1, 0),
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3,rad=-0.55", **arc), zorder=3)
ax.text(1.5, 0.50, r"$c$", fontsize=12, ha="center", va="bottom", color=VERM)

# b: Q leapfrogs 0 -> eps using P(eps/2) (below).
ax.annotate("", xy=(2, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3,rad=0.42", **arc), zorder=3)
ax.text(1.0, -0.56, r"$b$", fontsize=12, ha="center", va="top", color=VERM)

ax.set_xlim(-0.6, 2.6)
ax.set_ylim(-1.15, 1.0)

fig.savefig("../fig-redraw-021.pdf")
fig.savefig("../fig-redraw-021.png", dpi=200)
print("done 021")

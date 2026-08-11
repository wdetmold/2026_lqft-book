"""Redraw of fig-notes-060: schematic of a gauge-invariant observable built
with the Levi-Civita symbol in SU(3): three Wilson lines (paths of links)
running from x to y, with their colour indices contracted by epsilon symbols
at the endpoints.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

# three lattice (staircase) paths from x = (0, 0) to y = (10, 3)
paths = [
    # upper staircase
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (5, 4),
     (5, 5), (7, 5), (7, 4), (9, 4), (9, 3), (10, 3)],
    # middle staircase
    [(0, 0), (2, 0), (2, 1), (4, 1), (4, 2), (6, 2), (6, 3), (10, 3)],
    # lower path along the bottom
    [(0, 0), (0, -1), (10, -1), (10, 3)],
]
for p in paths:
    xs, ys = zip(*p)
    ax.plot(xs, ys, color=C_BLUE, lw=1.8, solid_joinstyle="round", zorder=2)

# endpoints and labels
for (px, py) in [(0, 0), (10, 3)]:
    ax.plot([px], [py], marker="o", ms=6, color=C_BLUE, zorder=3)
ax.text(-0.35, 0.55, r"$x$", color=C_BLUE, ha="right", va="center",
        fontsize=12)
ax.text(10.4, 3.55, r"$y$", color=C_BLUE, ha="left", va="center",
        fontsize=12)
ax.text(-0.75, -0.75, r"$\varepsilon$", color=C_BLUE, ha="right",
        va="center", fontsize=13)

ax.set_xlim(-1.8, 11.4)
ax.set_ylim(-1.8, 5.8)

fig.savefig("../fig-redraw-060.pdf")
fig.savefig("../fig-redraw-060.png", dpi=200)
print("done 060")

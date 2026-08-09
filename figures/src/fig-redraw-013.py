"""Redraw of fig-notes-013: temporal gauge in D = 2 on a lattice of infinite
extent.  Every temporal link (horizontal, red) is set to unity; the red lines
run off the edge of the picture.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_RED = "#D55E00"
C_GREEN = "#009E73"

NT, NS = 11, 5  # time slices (columns), spatial sites (rows)

fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.set_aspect("equal")
ax.axis("off")

# spatial links (green, vertical)
for x in range(NT):
    ax.plot([x, x], [-0.55, NS - 1 + 0.55], color=C_GREEN, lw=1.3, zorder=1)

# temporal links, all set to 1 (red, horizontal, extending off the lattice)
for y in range(NS):
    ax.plot([-0.85, NT - 1 + 0.85], [y, y], color=C_RED, lw=2.6, zorder=2)

ax.annotate(r"$U_4(n) = 1$", xy=(2.5, NS - 1), xytext=(3.6, NS + 0.35),
            color=C_RED, fontsize=10, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2, shrinkB=3))

ax.set_xlim(-1.1, NT - 1 + 1.1)
ax.set_ylim(-0.9, NS + 0.8)

fig.savefig("../fig-redraw-013.pdf")
fig.savefig("../fig-redraw-013.png", dpi=200)
print("done 013")

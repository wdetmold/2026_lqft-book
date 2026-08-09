"""Redraw of fig-notes-065: a large R x T Wilson loop built from lattice
links, defining the static quark potential. Static source Q at (R,0) and
antisource Qbar at (0,0) propagate a time T (horizontal direction)."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

GREEN = "#009E73"
BLUE = "#0072B2"

T, R = 6, 4  # temporal (horizontal) and spatial (vertical) extents, lattice units

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# perimeter of the loop
ax.plot([0, T, T, 0, 0], [R, R, 0, 0, R], color=GREEN, lw=2.0, zorder=2,
        solid_capstyle="round")

# link ticks: short marks across each edge at the lattice sites
tick = 0.10
for t in range(1, T):        # top and bottom edges
    ax.plot([t, t], [R - tick, R + tick], color=GREEN, lw=1.4)
    ax.plot([t, t], [-tick, tick], color=GREEN, lw=1.4)
for r in range(1, R):        # left and right edges
    ax.plot([-tick, tick], [r, r], color=GREEN, lw=1.4)
    ax.plot([T - tick, T + tick], [r, r], color=GREEN, lw=1.4)


# orientation arrows at mid-edge
def edge_arrow(x, y, dx, dy):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x - dx, y - dy),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.0,
                                mutation_scale=16))


edge_arrow(T / 2, R, 0.28, 0)    # top: increasing t
edge_arrow(T, R / 2, 0, -0.28)   # right: down
edge_arrow(T / 2, 0, -0.28, 0)   # bottom: decreasing t
edge_arrow(0, R / 2, 0, 0.28)    # left: up

# static sources at t = 0
ax.plot([0], [R], marker="o", ms=8, color=BLUE, zorder=4)
ax.plot([0], [0], marker="o", ms=8, color=BLUE, zorder=4)
ax.text(0.30, R + 0.28, r"$Q$", color=BLUE, fontsize=13,
        ha="left", va="bottom")
ax.text(0.34, -0.30, r"$\overline{Q}$", color=BLUE, fontsize=13,
        ha="left", va="top")

# corner coordinates (space, time)
ax.text(-0.30, R + 0.28, r"$(R,0)$", ha="right", va="bottom", fontsize=11)
ax.text(T + 0.30, R + 0.28, r"$(R,T)$", ha="left", va="bottom", fontsize=11)
ax.text(-0.30, -0.30, r"$(0,0)$", ha="right", va="top", fontsize=11)
ax.text(T + 0.30, -0.30, r"$(0,T)$", ha="left", va="top", fontsize=11)

ax.set_xlim(-1.7, 7.8)
ax.set_ylim(-1.1, 5.1)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-065.pdf")
fig.savefig("../fig-redraw-065.png", dpi=200)
print("done 065")

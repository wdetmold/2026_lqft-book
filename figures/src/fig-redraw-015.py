"""Redraw of fig-notes-015: temporal gauge with periodic boundary conditions.
Temporal links (red) between slices 0 ... N_t - 1 are set to unity; the link
wrapping around the boundary (green stubs) is identified:
U_{-4}^dag(n_t = 0) = U_4(n_t = N_t - 1).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import Ellipse, FancyArrowPatch

C_RED = "#D55E00"
C_GREEN = "#009E73"
C_BLUE = "#0072B2"

NT, NS = 11, 5  # time slices (columns 0 ... N_t - 1), spatial sites (rows)
L = NT - 1      # x coordinate of last slice

fig, ax = plt.subplots(figsize=(4.9, 3.6))
ax.set_aspect("equal")
ax.axis("off")

# spatial links (green, vertical) at each time slice
for x in range(NT):
    ax.plot([x, x], [-0.55, NS - 1 + 0.55], color=C_GREEN, lw=1.3, zorder=1)

# temporal links between slices 0 ... N_t-1, all set to 1 (red)
for y in range(NS):
    ax.plot([0, L], [y, y], color=C_RED, lw=2.6, zorder=2)

# the wrap-around temporal link: green stubs beyond both boundaries
for y in range(NS):
    ax.plot([-0.85, 0], [y, y], color=C_GREEN, lw=1.6, zorder=1)
    ax.plot([L, L + 0.85], [y, y], color=C_GREEN, lw=1.6, zorder=1)

# time-slice labels
for x, lab in [(0, "$0$"), (1, "$1$"), (2, "$2$"), (L, "$N_t-1$")]:
    ax.text(x, NS - 0.35, lab, color=C_BLUE, ha="center", va="bottom",
            fontsize=10)

# identification of the two ends of the bottom wrap-around stubs
for cx in (-0.85, L + 0.85):
    ax.add_patch(Ellipse((cx, 0), 0.85, 0.55, fill=False, color=C_BLUE,
                         lw=1.6, zorder=3))
ax.add_patch(FancyArrowPatch((-0.9, -0.28), (L + 0.9, -0.28),
                             arrowstyle="-", connectionstyle="arc3,rad=0.22",
                             color=C_BLUE, lw=1.6, zorder=3))
ax.text(0.5 * L, -1.75, "identified", color=C_BLUE, ha="center", va="top",
        fontsize=10)
ax.text(0.5 * L, -2.35,
        r"$U_{-4}^{\dagger}(n_t = 0) = U_4(n_t = N_t - 1)$",
        color=C_BLUE, ha="center", va="top", fontsize=10)

ax.set_xlim(-1.6, L + 1.6)
ax.set_ylim(-3.4, NS + 0.4)

fig.savefig("../fig-redraw-015.pdf")
fig.savefig("../fig-redraw-015.png", dpi=200)
print("done 015")

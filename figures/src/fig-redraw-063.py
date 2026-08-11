"""Redraw of fig-notes-063: the time-space plaquette appearing in the
exponent of the gauge transfer-matrix kernel,
U_m(n,t) U_4(n+m,t) U_m^dag(n,t+1) U_4^dag(n,t),
traversed counterclockwise in the (m-hat, t-hat) plane.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import FancyArrowPatch

C_RED = "#D55E00"
C_GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.set_aspect("equal")
ax.axis("off")

S = 2.0  # plaquette side
bl, br, tr, tl = (0, 0), (S, 0), (S, S), (0, S)

# lattice grid through the plaquette corners (green)
for x in (0, S):
    ax.plot([x, x], [-0.85, S + 0.85], color=C_GREEN, lw=1.3, zorder=1)
for y in (0, S):
    ax.plot([-0.85, S + 0.85], [y, y], color=C_GREEN, lw=1.3, zorder=1)

# directed links of the plaquette (red, counterclockwise)
for (a, b) in [(bl, br), (br, tr), (tr, tl), (tl, bl)]:
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=15,
                                 color=C_RED, lw=2.2, zorder=3,
                                 shrinkA=0, shrinkB=4))

# link labels (red)
ax.text(S / 2, -0.30, r"$U_m(\vec{n},t)$", color=C_RED, ha="center",
        va="top", fontsize=10)
ax.text(S + 0.30, S / 2, r"$U_4(\vec{n}+\hat{m},t)$", color=C_RED,
        ha="left", va="center", fontsize=10)
ax.text(S / 2, S + 0.30, r"$U_m^{\dagger}(\vec{n},t+1)$", color=C_RED,
        ha="center", va="bottom", fontsize=10)
ax.text(-0.30, S / 2, r"$U_4^{\dagger}(\vec{n},t)$", color=C_RED,
        ha="right", va="center", fontsize=10)

# coordinate axes (m-hat, t-hat)
ox, oy = -3.4, 0.1
ax.add_patch(FancyArrowPatch((ox, oy), (ox + 0.9, oy), arrowstyle="-|>",
                             mutation_scale=12, color=C_RED, lw=1.6))
ax.add_patch(FancyArrowPatch((ox, oy), (ox, oy + 0.9), arrowstyle="-|>",
                             mutation_scale=12, color=C_RED, lw=1.6))
ax.text(ox + 1.05, oy, r"$\hat{m}$", color=C_RED, ha="left", va="center",
        fontsize=11)
ax.text(ox, oy + 1.05, r"$\hat{t}$", color=C_RED, ha="center", va="bottom",
        fontsize=11)

ax.set_xlim(-3.8, S + 2.6)
ax.set_ylim(-1.2, S + 1.2)

fig.savefig("../fig-redraw-063.pdf")
fig.savefig("../fig-redraw-063.png", dpi=200)
print("done 063")

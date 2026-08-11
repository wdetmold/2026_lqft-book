"""Redraw of fig-notes-043: simple blocking of a lattice, a' = 2a.

Fine-lattice sites n in Lambda (dots, spacing a) grouped into 2x2 blocks
(shaded squares); each block carries a blocked site n_B in Lambda_B
(crosses, spacing a' = 2a) at its centre.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

CBLUE = "#0072B2"
CRED = "#D55E00"

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# Shaded 2x2 blocks (hypercubes around the blocked sites).
pad = 0.32
for bx in (0.5, 2.5):
    for by in (0.5, 2.5):
        ax.add_patch(plt.Rectangle((bx - 0.5 - pad, by - 0.5 - pad),
                                   1 + 2 * pad, 1 + 2 * pad,
                                   facecolor=CRED, alpha=0.13,
                                   edgecolor="none", zorder=1))
        ax.plot(bx, by, "x", ms=8, mew=2.0, color=CRED, zorder=3)

# Fine-lattice sites.
for x in range(4):
    for y in range(4):
        ax.plot(x, y, "o", ms=5, color=CBLUE, zorder=3)

# Labels with arrows.
ax.annotate(r"$n \in \Lambda$", xy=(3.0, 3.0), xytext=(4.1, 3.55),
            color=CBLUE, fontsize=12, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=CBLUE, lw=1.2,
                            connectionstyle="arc3,rad=0.2"))
ax.annotate(r"$n_B \in \Lambda_B$", xy=(2.55, 2.45), xytext=(4.1, 2.1),
            color=CRED, fontsize=12, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=CRED, lw=1.2,
                            connectionstyle="arc3,rad=-0.2"))

# Spacings: a between neighbouring fine sites, a' = 2a between blocked sites.
ax.annotate("", xy=(3, -0.75), xytext=(2, -0.75),
            arrowprops=dict(arrowstyle="<|-|>", color=CBLUE, lw=1.2))
ax.text(2.5, -0.95, r"$a$", color=CBLUE, fontsize=12, ha="center", va="top")
ax.annotate("", xy=(2.5, -1.55), xytext=(0.5, -1.55),
            arrowprops=dict(arrowstyle="<|-|>", color=CRED, lw=1.2))
ax.text(1.5, -1.75, r"$a' = 2a$", color=CRED, fontsize=12, ha="center", va="top")

ax.set_xlim(-1.1, 6.1)
ax.set_ylim(-2.3, 4.1)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-043.pdf")
fig.savefig("../fig-redraw-043.png", dpi=200)
print("done")

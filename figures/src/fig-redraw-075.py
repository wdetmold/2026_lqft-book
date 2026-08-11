"""Redraw of fig-notes-075: the assignment of the mu-nu plaquette (and the
links) to the half lattice.  Full-lattice sites are dots; the cells (x,{}),
(x,{1}), (x,{2}) and (x,{1,2}) are marked as crosses on the half lattice
(direction 1 vertical, direction 2 horizontal, as in the hand sketch).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

VERM = "#D55E00"
BLUE = "#0072B2"
GRAY = "0.65"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# Full lattice.
lo, hi, pad = 0, 3, 0.35
for k in range(lo, hi + 1):
    ax.plot([lo - pad, hi + pad], [k, k], color=GRAY, lw=0.8, zorder=1)
    ax.plot([k, k], [lo - pad, hi + pad], color=GRAY, lw=0.8, zorder=1)

# Full-lattice sites: x and its neighbours around the plaquette.
ax.scatter([1, 1, 2, 2], [1, 2, 1, 2], s=38, color=BLUE, zorder=4)

# Dotted guides from x to the neighbouring sites, through the half-lattice points.
dot = dict(color=VERM, lw=1.1, ls=(0, (1, 2)), zorder=3)
ax.plot([1, 1], [1, 2], **dot)
ax.plot([1, 2], [1, 1], **dot)
ax.plot([1, 2], [1, 2], **dot)

# Half-lattice points: site, the two link midpoints, the plaquette centre.
hx = [1.0, 1.0, 1.5, 1.5]
hy = [1.0, 1.5, 1.0, 1.5]
ax.scatter(hx, hy, s=55, color=VERM, marker="x", lw=1.6, zorder=5)

lab = dict(fontsize=10, color="k", zorder=6)
ax.text(0.88, 0.80, r"$(x,\{\})$", ha="right", va="top", **lab)
ax.text(0.82, 1.5, r"$(x,\{1\})$", ha="right", va="center", **lab)
ax.text(1.5, 0.80, r"$(x,\{2\})$", ha="center", va="top", **lab)
ax.annotate(r"$(x,\{1,2\})$", xy=(1.62, 1.55), xytext=(2.55, 2.15),
            fontsize=10, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.1,
                            connectionstyle="arc3,rad=-0.25"), zorder=6)

ax.set_xlim(-1.1, 4.6)
ax.set_ylim(-0.7, 3.6)

fig.savefig("../fig-redraw-075.pdf")
fig.savefig("../fig-redraw-075.png", dpi=200)
print("done 075")

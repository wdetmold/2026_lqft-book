"""Redraw of fig-notes-031: the vertex function computed for RI/MOM-type
renormalisation.  Incoming quark with momentum p1, outgoing quark with
momentum p2, and the operator insertion (dashed line, momentum p2 - p1)
at the shaded vertex blob.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle

BLUE = "#0072B2"
VERM = "#D55E00"
INK = "0.15"
GREY = "0.82"

fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

vtx = np.array([0.0, 0.0])

# incoming quark line, momentum p1
ax.plot([-1.7, -0.02], [-0.75, -0.01], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
ax.annotate("", xy=(-0.78, -0.345), xytext=(-1.0, -0.44),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, shrinkA=0,
                            shrinkB=0, mutation_scale=13), zorder=3)
ax.text(-1.35, -0.35, r"$p_1$", ha="center", va="bottom", fontsize=13,
        color=INK)

# outgoing quark line, momentum p2
ax.plot([0.02, 1.7], [-0.01, -0.75], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
ax.annotate("", xy=(1.0, -0.44), xytext=(0.78, -0.345),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, shrinkA=0,
                            shrinkB=0, mutation_scale=13), zorder=3)
ax.text(1.35, -0.35, r"$p_2$", ha="center", va="bottom", fontsize=13,
        color=INK)

# operator insertion: dashed line carrying momentum p2 - p1
ax.plot([0.0, 0.0], [1.35, 0.45], color=VERM, lw=1.4, ls=(0, (4, 3)),
        zorder=2)
ax.annotate("", xy=(0.0, 0.3), xytext=(0.0, 0.5),
            arrowprops=dict(arrowstyle="-|>", color=VERM, shrinkA=0,
                            shrinkB=0, mutation_scale=13), zorder=3)
ax.text(0.16, 0.95, r"$p_2 - p_1$", ha="left", va="center", fontsize=13,
        color=INK)

# vertex blob
ax.add_patch(Circle(vtx, 0.24, facecolor=GREY, edgecolor=INK, lw=1.1,
                    zorder=4))

ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-1.1, 1.6)

fig.savefig("../fig-redraw-031.pdf")
fig.savefig("../fig-redraw-031.png", dpi=200)
print("done")

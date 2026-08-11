"""Redraw of fig-notes-005: diagrammatic representation of the connected
three-point function G^{123}: a 1PI vertex blob Gamma^(3) with three
propagator legs G^{11'}, G^{22'}, G^{33'}; outer ends labelled 1, 2, 3 and
the ends attached to the blob labelled 1', 2', 3'.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle

C = "#0072B2"

fig, ax = plt.subplots(figsize=(3.2, 3.2))
ax.set_aspect("equal")
ax.set_axis_off()

R = 0.34    # blob radius
L = 1.05    # outer end radius

blob = Circle((0, 0), R, facecolor="0.92", edgecolor=C, lw=1.6, zorder=3)
ax.add_patch(blob)

# legs at 90 (2), 210 (1), 330 (3) degrees
for ang, lab in [(90, "2"), (210, "1"), (330, "3")]:
    t = np.deg2rad(ang)
    ux, uy = np.cos(t), np.sin(t)
    ax.plot([R * ux, L * ux], [R * uy, L * uy], color=C, lw=1.6,
            solid_capstyle="round", zorder=2)
    # outer label just beyond the leg end
    ax.text(1.22 * ux, 1.22 * uy, f"${lab}$", color="k",
            ha="center", va="center", fontsize=12)
    # primed label beside the point where the leg meets the blob
    px, py = 1.32 * R * ux, 1.32 * R * uy
    # offset perpendicular to the leg so the label sits beside it
    ox, oy = -uy, ux
    ax.text(px + 0.14 * ox, py + 0.14 * oy, f"${lab}'$", color="k",
            ha="center", va="center", fontsize=10)

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)

fig.savefig("../fig-redraw-005.pdf")
fig.savefig("../fig-redraw-005.png", dpi=200)

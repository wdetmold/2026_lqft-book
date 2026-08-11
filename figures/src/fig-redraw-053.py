"""Redraw of fig-notes-053: diagrammatic representation of the connected
four-point function,

  G^{1234} = - (four-leg 1PI blob)
             + (two three-leg blobs joined by a propagator)_{x 3 perms}
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle

C = "#0072B2"

fig, ax = plt.subplots(figsize=(7.4, 2.0))
ax.set_aspect("equal")
ax.set_axis_off()

R = 0.30    # blob radius
LEG = 0.62  # leg length beyond the blob edge


def blob(xc, yc, angles):
    """Draw a blob at (xc, yc) with external legs at the given angles."""
    ax.add_patch(Circle((xc, yc), R, facecolor="0.92", edgecolor=C,
                        lw=1.5, zorder=3))
    for ang in angles:
        t = np.deg2rad(ang)
        ux, uy = np.cos(t), np.sin(t)
        ax.plot([xc + R * ux, xc + (R + LEG) * ux],
                [yc + R * uy, yc + (R + LEG) * uy],
                color=C, lw=1.5, solid_capstyle="round", zorder=2)


# G^{1234}  =  -
ax.text(-0.4, 0.0, r"$G^{1234}\;=\;-$", ha="right", va="center",
        fontsize=13)

# first term: single blob with four legs (X arrangement)
blob(0.6, 0.0, [45, 135, 225, 315])

# +
ax.text(1.85, 0.0, "$+$", ha="center", va="center", fontsize=13)

# second term: two blobs joined by an internal propagator, two legs each
x1, x2 = 3.45, 4.85
blob(x1, 0.0, [135, 225])
blob(x2, 0.0, [45, 315])
ax.plot([x1 + R, x2 - R], [0, 0], color=C, lw=1.5,
        solid_capstyle="round", zorder=2)

# large parentheses around the second term, with "x 3 perms" subscript
ax.text(x1 - R - LEG - 0.28, 0.0, "(", ha="center", va="center",
        fontsize=30)
ax.text(x2 + R + LEG + 0.28, 0.0, ")", ha="center", va="center",
        fontsize=30)
ax.text(x2 + R + LEG + 0.52, -0.72, r"$\times\,3\ \mathrm{perms}$",
        ha="left", va="center", fontsize=10)

ax.set_xlim(-2.6, 7.4)
ax.set_ylim(-1.15, 1.15)

fig.savefig("../fig-redraw-053.pdf")
fig.savefig("../fig-redraw-053.png", dpi=200)

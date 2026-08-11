"""Redraw of fig-notes-085: elastic electron-proton scattering.
d sigma / d Omega (ep -> ep) ~ | amplitude |^2 where the amplitude
diagram has an electron line, a photon exchanged with the proton, and a
hadronic blob on the proton (three-quark) line: the hadronic matrix
element.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Ellipse

BLUE = "#0072B2"
VERM = "#D55E00"
INK = "0.15"
GREY = "0.82"


def wavy(p0, p1, amp=0.07, waves=4.5, n=400):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    t = np.linspace(0, 1, n)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nv = np.array([-u[1], u[0]])
    return (p0[None, :] + t[:, None] * d[None, :]
            + amp * np.sin(2 * np.pi * waves * t)[:, None] * nv[None, :])


fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

# prefactor text
ax.text(-2.35, 0.15,
        r"$\dfrac{d\sigma}{d\Omega}\,(ep \to ep)\ \sim$",
        ha="right", va="center", fontsize=12, color=INK)

# ---- amplitude diagram --------------------------------------------------
vtx = np.array([0.0, 0.75])       # electron-photon vertex
blob = np.array([0.15, -0.55])    # hadronic blob centre

# electron line: in from upper left, out to upper right
ax.plot([-1.45, vtx[0]], [1.45, vtx[1]], color=BLUE, lw=1.5,
        solid_capstyle="round", zorder=2)
ax.plot([vtx[0], 1.45], [vtx[1], 1.45], color=BLUE, lw=1.5,
        solid_capstyle="round", zorder=2)
ax.annotate("", xy=(-0.65, 1.06), xytext=(-0.85, 1.16),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, shrinkA=0,
                            shrinkB=0, mutation_scale=12), zorder=3)
ax.annotate("", xy=(0.85, 1.16), xytext=(0.65, 1.06),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, shrinkA=0,
                            shrinkB=0, mutation_scale=12), zorder=3)

# photon: wavy line from electron vertex down to the hadronic blob
w = wavy(vtx, blob + np.array([0.0, 0.30]))
ax.plot(w[:, 0], w[:, 1], color=VERM, lw=1.4, zorder=2)

# proton: three quark lines through the shaded blob
for dy in (0.11, 0.0, -0.11):
    ax.plot([-1.45, 1.55], [-0.72 + dy, -0.50 + dy], color=BLUE, lw=1.4,
            solid_capstyle="round", zorder=2)
ax.add_patch(Ellipse(blob, 0.62, 0.5, angle=8.0, facecolor=GREY,
                     edgecolor=INK, lw=1.0, zorder=3))

# ---- modulus-squared bars ----------------------------------------------
for xb in (-1.95, 1.95):
    ax.plot([xb, xb], [-1.15, 1.55], color=INK, lw=1.2, zorder=1)
ax.text(2.08, 1.55, r"$2$", ha="left", va="top", fontsize=12, color=INK)

ax.set_xlim(-5.4, 2.6)
ax.set_ylim(-1.5, 1.9)

fig.savefig("../fig-redraw-085.pdf")
fig.savefig("../fig-redraw-085.png", dpi=200)
print("done")

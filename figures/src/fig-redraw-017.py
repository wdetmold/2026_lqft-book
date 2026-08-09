"""Redraw of fig-notes-017: 1D illustration of the doubling theorem,
companion of fig-redraw-018. Alternatively, zeros of the periodic
(Fourier transform of the) kernel F could appear as double zeros, which
would not correspond to a linear dispersion relation.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

RED = "#D55E00"
BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(3.3, 2.7))
ax.set_aspect(1.05)
ax.axis("off")

L = np.pi  # k axis in units of 1/a

# k axis as an arrow, Brillouin-zone edges as vertical lines
ax.annotate("", xy=(L + 0.75, 0), xytext=(-L - 0.45, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=13))
ax.annotate("", xy=(0, 2.05), xytext=(0, -0.55),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=13))
ax.plot([-L, -L], [-0.35, 1.85], color="black", lw=0.8)
ax.plot([L, L], [-0.35, 1.85], color="black", lw=0.8)

ax.text(L + 0.8, -0.06, r"$k$", fontsize=12, ha="left", va="center")
ax.text(0.22, 2.0, r"$\tilde{F}$", fontsize=12, ha="left", va="center")
ax.text(-L, -0.48, r"$-\pi/a$", fontsize=10, ha="center", va="top")
ax.text(L, -0.48, r"$\pi/a$", fontsize=10, ha="center", va="top")
ax.text(-0.13, -0.48, r"$0$", fontsize=10, ha="center", va="top")

# periodic curve with a single double zero (tangent to the axis)
k0 = 0.5
k = np.linspace(-L, L, 400)
F = 0.75 * (1 - np.cos(k - k0)) + 0.10 * (1 - np.cos(2 * (k - k0)))
ax.plot(k, F, color=RED, lw=1.8, zorder=3)
ax.plot([k0], [0], "o", ms=5, color=RED, zorder=4)

# annotation with arrow to the double zero
ax.annotate("", xy=(k0 + 0.06, -0.14), xytext=(1.05, -1.05),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2,
                            mutation_scale=12,
                            connectionstyle="arc3,rad=0.2"))
ax.text(0.65, -1.2, "as double zeros which\nwould not correspond to\n"
        "a linear dispersion relation",
        fontsize=9, color=BLUE, ha="center", va="top", linespacing=1.4)

ax.set_xlim(-L - 0.55, L + 1.05)
ax.set_ylim(-2.25, 2.2)

fig.savefig("../fig-redraw-017.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-017.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 017")

"""Redraw of fig-notes-018: 1D illustration of the doubling theorem. For a
periodic (Fourier transform of the) kernel F, zeros over the Brillouin zone
[-pi/a, pi/a] appear as two zeros with opposite signed slopes.
Companion of fig-redraw-017 (double-zero case); the two sit side by side.
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

# periodic curve with two simple zeros of opposite signed slopes
k = np.linspace(-L, L, 400)
F = 0.5 - np.cos(k) + 0.10 * np.sin(2 * k) + 0.07 * np.cos(3 * k)
ax.plot(k, F, color=RED, lw=1.8, zorder=3)

# mark the zeros
kz = []
for i in range(len(k) - 1):
    if F[i] * F[i + 1] < 0:
        kz.append(k[i] - F[i] * (k[i + 1] - k[i]) / (F[i + 1] - F[i]))
ax.plot(kz, [0, 0], "o", ms=5, color=RED, zorder=4)

# annotation with arrows to both zeros
ax.annotate("", xy=(kz[0], -0.14), xytext=(-0.72, -1.28),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2,
                            mutation_scale=12,
                            connectionstyle="arc3,rad=-0.25"))
ax.annotate("", xy=(kz[1], -0.14), xytext=(0.42, -1.28),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2,
                            mutation_scale=12,
                            connectionstyle="arc3,rad=0.25"))
ax.text(-0.15, -1.42, "as two zeros with\nopposite signed slopes",
        fontsize=9, color=BLUE, ha="center", va="top", linespacing=1.4)

ax.set_xlim(-L - 0.55, L + 1.05)
ax.set_ylim(-2.25, 2.2)

fig.savefig("../fig-redraw-018.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-018.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 018")

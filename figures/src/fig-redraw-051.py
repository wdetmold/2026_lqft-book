"""Redraw of fig-notes-051: anticipated phase diagram of the gauge-fixed
(Abelian) chiral gauge theory in the (kappa-tilde, rho) plane.  A continuous
transition line rho_c(kappa~) separates m_A^2 > 0 (above) from m_A^2 < 0
(below); a Coulomb phase pocket sits at small kappa~; the large-kappa~ band
is where perturbative control holds."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

GREEN = "#009E73"
RED = "#D55E00"
INK = "0.15"

fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.axis("off")

# ---- shaded band: perturbative control at large kappa~ ------------------
ax.axvspan(6.2, 8.8, color=RED, alpha=0.10, lw=0, zorder=0)
ax.text(7.5, 3.35, "perturbative\ncontrol", color=RED, fontsize=10,
        ha="center", va="bottom", linespacing=1.1)

# ---- axes ---------------------------------------------------------------
ax.annotate("", xy=(9.6, 0), xytext=(-1.3, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9,
                            mutation_scale=12), zorder=2)
ax.annotate("", xy=(0, 3.6), xytext=(0, -4.3),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9,
                            mutation_scale=12), zorder=2)
ax.text(-0.35, 3.35, r"$\rho$", fontsize=13, ha="right", va="center")
ax.text(9.65, 0.30, r"$\tilde{\kappa}$", fontsize=13, ha="left",
        va="bottom")

# ---- transition line rho_c(kappa~), flat at large kappa~ ----------------
x = np.linspace(-1.0, 9.3, 300)
rho_c = 0.85 + 1.55 * np.exp(-(x + 1.0) / 1.1)
ax.plot(x, rho_c, color=GREEN, lw=2.0, solid_capstyle="round", zorder=3)
ax.text(5.3, 1.15, r"$\rho_c(\tilde{\kappa})$", color=GREEN, fontsize=12,
        ha="center", va="bottom")

# ---- second boundary running to the lower left --------------------------
t = np.linspace(0, 1, 200)
bx = -1.35 + 2.75 * t
by = 1.2 - 5.0 * t - 1.4 * t**2
ax.plot(bx, by, color=GREEN, lw=2.0, solid_capstyle="round", zorder=3)

# ---- Coulomb phase pocket (tilted closed loop) --------------------------
th = np.linspace(0, 2 * np.pi, 300)
a, b, ang = 2.05, 0.90, np.deg2rad(-16)
ex = a * np.cos(th)
ey = b * np.sin(th)
cx = 1.55 + ex * np.cos(ang) - ey * np.sin(ang)
cy = -0.95 + ex * np.sin(ang) + ey * np.cos(ang)
ax.plot(cx, cy, color=GREEN, lw=2.0, zorder=3)
ax.text(1.75, -1.05, "Coulomb", color=GREEN, fontsize=10,
        ha="center", va="center", style="italic")

# ---- region labels ------------------------------------------------------
ax.text(4.4, 2.55, r"$m_A^2 > 0$", color=GREEN, fontsize=12,
        ha="center", va="center")
ax.text(7.5, -2.3, r"$m_A^2 < 0$", color=GREEN, fontsize=12,
        ha="center", va="center")

ax.set_xlim(-1.7, 10.3)
ax.set_ylim(-4.6, 4.4)

fig.savefig("../fig-redraw-051.pdf")
fig.savefig("../fig-redraw-051.png", dpi=200)
print("done 051")

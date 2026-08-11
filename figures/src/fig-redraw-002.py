import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

# Redraw of fig-notes-002.jpg: dispersion relation omega(p) vs |p|.
# Three curves: m = 0 continuum (omega = |p|), m != 0 continuum
# (omega = sqrt(m^2 + p^2)), and m != 0 lattice
# (cosh omega = 1 + (m^2 + 4 sin^2(p/2))/2), which flattens at the
# edge of the Brillouin zone.

import numpy as np

C_MASSIVE = "#0072B2"   # m != 0 continuum
C_MASSLESS = "#D55E00"  # m = 0 continuum
C_LATTICE = "#009E73"   # m != 0 lattice

fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.axis("off")

m = 0.9
p = np.linspace(-np.pi, np.pi, 400)

w_massless = np.abs(p)
w_massive = np.sqrt(m**2 + p**2)
w_lattice = np.arccosh(1.0 + 0.5 * (m**2 + 4.0 * np.sin(p / 2.0)**2))

ax.plot(p, w_massive, color=C_MASSIVE, lw=1.6, zorder=3)
ax.plot(p, w_massless, color=C_MASSLESS, lw=1.6, zorder=3)
ax.plot(p, w_lattice, color=C_LATTICE, lw=1.6, zorder=3)

# axes as arrows through the origin (y axis extends below zero as in notes)
ax.annotate("", xy=(4.15, 0.0), xytext=(-3.65, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.annotate("", xy=(0.0, 3.85), xytext=(0.0, -1.15),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0))
ax.text(0.14, 3.80, r"$\omega(\vec{p}\,)$", ha="left", va="center",
        fontsize=11)
ax.text(3.95, -0.32, r"$|\vec{p}\,|$", ha="center", va="top", fontsize=11)

# direct labels
ax.text(3.30, 3.55, r"$m\neq 0$ continuum", color=C_MASSIVE, ha="left",
        va="center", fontsize=9.5)
ax.text(3.30, 3.12, r"$m=0$ continuum", color=C_MASSLESS, ha="left",
        va="center", fontsize=9.5)
ax.text(3.30, 1.88, r"$m\neq 0$ lattice", color=C_LATTICE, ha="left",
        va="center", fontsize=9.5)

ax.set_xlim(-3.8, 6.3)
ax.set_ylim(-1.3, 4.0)

fig.savefig("../fig-redraw-002.pdf")
fig.savefig("../fig-redraw-002.png", dpi=200)

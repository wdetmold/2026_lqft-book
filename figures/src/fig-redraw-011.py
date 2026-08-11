"""Redraw of fig-notes-011: the link U_mu(n) and the links (1), (2), (3) used
in the successive changes of variables, together with the four associated
plaquettes P_{mu nu}(n), P_{mu nu}(n - mu), P_{mu nu}(n - nu) and
P_{mu nu}(n - mu - nu).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_GREEN = "#009E73"
C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.set_aspect("equal")
ax.axis("off")

# ---- background lattice ----------------------------------------------------
for k in (-1, 0, 1):
    ax.plot([-1.5, 1.5], [k, k], color="0.75", lw=0.8, zorder=0)
    ax.plot([k, k], [-1.5, 1.5], color="0.75", lw=0.8, zorder=0)
for i in (-1, 0, 1):
    for j in (-1, 0, 1):
        ax.plot([i], [j], marker="o", ms=3, color="0.55", zorder=1)

# site n
ax.plot([0], [0], marker="o", ms=6, color=C_BLUE, zorder=5)
ax.text(-0.10, -0.13, r"$n$", color=C_BLUE, ha="right", va="top",
        fontsize=11)

# ---- the link U_mu(n) (directed) -------------------------------------------
ax.plot([0, 1], [0, 0], color=C_RED, lw=2.2, zorder=3,
        solid_capstyle="round")
ax.annotate("", xy=(0.62, 0), xytext=(0.58, 0),
            arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2.2,
                            mutation_scale=15), zorder=4)
ax.text(0.56, -0.12, r"$U_\mu(n)$", color=C_RED, ha="center", va="top",
        fontsize=10)

# ---- links used in the changes of variables (dotted, numbered) -------------
links = [((0, 0), (0, 1), "1", (-0.20, 0.80)),    # U_nu(n)
         ((-1, 0), (0, 0), "2", (-0.80, 0.18)),   # U_mu(n - mu)
         ((0, -1), (0, 0), "3", (-0.20, -0.80))]  # U_nu(n - nu)
for (x0, y0), (x1, y1), num, (tx, ty) in links:
    ax.plot([x0, x1], [y0, y1], color=C_GREEN, lw=2.2, zorder=3,
            ls=(0, (1, 1.4)))
    ax.text(tx, ty, num, color=C_GREEN, ha="center", va="center",
            fontsize=8, zorder=5,
            bbox=dict(boxstyle="circle,pad=0.25", facecolor="white",
                      edgecolor=C_GREEN, lw=1.0))

# ---- the four associated plaquettes (counter-clockwise loops) --------------
def loop(cx, cy, label):
    rx, ry = 0.42, 0.25
    th = np.radians(np.linspace(-55, 235, 120))
    ax.plot(cx + rx * np.cos(th), cy + ry * np.sin(th), color=C_GREEN,
            lw=1.1, zorder=2)
    t1, t0 = np.radians(235), np.radians(231)
    ax.annotate("", xy=(cx + rx * np.cos(t1), cy + ry * np.sin(t1)),
                xytext=(cx + rx * np.cos(t0), cy + ry * np.sin(t0)),
                arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=1.1,
                                mutation_scale=10), zorder=2)
    ax.text(cx, cy, label, color=C_GREEN, ha="center", va="center",
            fontsize=7.5, zorder=2)


loop(-0.5, 0.5, r"$P_{\mu\nu}(n-\hat{\mu})$")
loop(0.5, 0.5, r"$P_{\mu\nu}(n)$")
loop(-0.5, -0.5, r"$P_{\mu\nu}(n-\hat{\mu}-\hat{\nu})$")
loop(0.5, -0.5, r"$P_{\mu\nu}(n-\hat{\nu})$")

ax.set_xlim(-1.72, 1.72)
ax.set_ylim(-1.65, 1.65)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-011.pdf")
fig.savefig("../fig-redraw-011.png", dpi=200)
print("done 011")

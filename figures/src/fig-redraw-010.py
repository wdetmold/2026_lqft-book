"""Redraw of fig-notes-010: the elementary plaquette U_{mu nu}(n), the
counter-clockwise product of four directed links starting at site n:
U_mu(n) U_nu(n+mu) U_mu^dag(n+nu) U_nu^dag(n).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_RED = "#D55E00"
C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# ---- background lattice ----------------------------------------------------
for k in (0, 1, 2):
    ax.plot([-0.5, 2.5], [k, k], color="0.75", lw=0.8, zorder=0)
    ax.plot([k, k], [-0.5, 2.5], color="0.75", lw=0.8, zorder=0)
for i in (0, 1, 2):
    for j in (0, 1, 2):
        ax.plot([i], [j], marker="o", ms=3, color="0.55", zorder=1)

# ---- the plaquette: counter-clockwise directed links from n = (1, 1) -------
edges = [((1, 1), (2, 1)),   # U_mu(n)
         ((2, 1), (2, 2)),   # U_nu(n + mu)
         ((2, 2), (1, 2)),   # U_mu^dag(n + nu)
         ((1, 2), (1, 1))]   # U_nu^dag(n)
for (x0, y0), (x1, y1) in edges:
    ax.plot([x0, x1], [y0, y1], color=C_RED, lw=2.0, zorder=3,
            solid_capstyle="round")
    xm, ym = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    dx, dy = 0.001 * (x1 - x0), 0.001 * (y1 - y0)
    ax.annotate("", xy=(xm + dx, ym + dy), xytext=(xm - dx, ym - dy),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2.0,
                                mutation_scale=15), zorder=4)

# site n
ax.plot([1], [1], marker="o", ms=7, color=C_BLUE, zorder=5)
ax.text(0.88, 0.86, r"$n$", color=C_BLUE, ha="right", va="top", fontsize=12)

# ---- direction indicators --------------------------------------------------
ax.annotate("", xy=(1.35, -0.75), xytext=(0.65, -0.75),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.3,
                            mutation_scale=12))
ax.text(1.47, -0.75, r"$\hat{\mu}$", color=C_BLUE, ha="left", va="center",
        fontsize=12)
ax.annotate("", xy=(-0.75, 1.35), xytext=(-0.75, 0.65),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.3,
                            mutation_scale=12))
ax.text(-0.75, 1.47, r"$\hat{\nu}$", color=C_BLUE, ha="center", va="bottom",
        fontsize=12)

ax.set_xlim(-1.05, 2.75)
ax.set_ylim(-1.05, 2.75)

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-010.pdf")
fig.savefig("../fig-redraw-010.png", dpi=200)
print("done 010")

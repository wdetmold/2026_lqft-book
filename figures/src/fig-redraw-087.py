"""Redraw of fig-notes-087: a choice for the blocking kernel Q_mu(n_B) in
SU(N) Yang-Mills blocking (scale factor 2): straight two-link term plus
c times the sum over nu != mu of the up- and down-staple two-link paths."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

BLUE = "#0072B2"
GREEN = "#009E73"
INK = "0.15"

fig, ax = plt.subplots(figsize=(7.2, 1.5))
ax.set_aspect("equal")
ax.axis("off")


def staple(ax, x0, y0, up=+1, s=0.42):
    """Two-link staple path: step in nu, two steps in mu, step back."""
    xs = [x0, x0, x0 + s, x0 + 2 * s, x0 + 2 * s]
    ys = [y0, y0 + up * s, y0 + up * s, y0 + up * s, y0]
    ax.plot(xs, ys, color=BLUE, lw=1.6, solid_capstyle="round", zorder=2)
    ax.plot(xs, ys, ls="none", marker="o", ms=4, color=BLUE, zorder=3)


# ---- equation text ------------------------------------------------------
ax.text(0.0, 0.0,
        r"$Q_\mu(n_B)\ =\ (1-6c)\,U_\mu(n)\,U_\mu(n+\hat{\mu})"
        r"\ +\ c\sum_{\nu\neq\mu}$",
        fontsize=13, ha="left", va="center", color=INK)

# ---- up-staple + down-staple --------------------------------------------
staple(ax, 6.55, -0.21, up=+1)
ax.text(7.70, 0.0, r"$+$", fontsize=13, ha="center", va="center",
        color=INK)
staple(ax, 8.00, 0.21, up=-1)

# ---- direction key (nu up, mu right) ------------------------------------
kx, ky = 5.90, -0.80
ax.annotate("", xy=(kx, ky + 0.38), xytext=(kx, ky),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0,
                            mutation_scale=10))
ax.annotate("", xy=(kx + 0.38, ky), xytext=(kx, ky),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0,
                            mutation_scale=10))
ax.text(kx - 0.10, ky + 0.34, r"$\nu$", color=GREEN, fontsize=10,
        ha="right", va="center")
ax.text(kx + 0.46, ky - 0.02, r"$\mu$", color=GREEN, fontsize=10,
        ha="left", va="center")

ax.set_xlim(-0.15, 9.2)
ax.set_ylim(-0.95, 0.75)

fig.savefig("../fig-redraw-087.pdf")
fig.savefig("../fig-redraw-087.png", dpi=200)
print("done 087")

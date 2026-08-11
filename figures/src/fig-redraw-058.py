"""Redraw of fig-notes-058: integrating the links of the tiled Wilson loop
column by column using int dU U_ab U^dag_cd = (1/N) delta_ad delta_bc.
Top row: four panels showing the tiling collapsing into narrow vertical
strips, picking up factors (1/N)^R ... (1/N)^{RT}, last trace = N.
Bottom: the graphical identity int dU tr[V U^dag] tr[U W] = (1/N) tr[VW]
(two plaquettes sharing a link merge into one loop).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_GREEN = "#009E73"
C_BLUE = "#0072B2"
C_RED = "#D55E00"

T, R = 4, 3  # loop dimensions in lattice units

fig, ax = plt.subplots(figsize=(6.8, 2.9))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, color=C_GREEN, frac=0.5, ms=9):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    m = a + frac * d
    eps = 1e-3 * d
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def loop(x0, y0=0.0):
    ax.add_patch(plt.Rectangle((x0, y0), T, R, facecolor="none",
                               edgecolor=C_GREEN, lw=1.7, joinstyle="round"))
    arrow_on((x0, y0), (x0, y0 + R))
    arrow_on((x0, y0 + R), (x0 + T, y0 + R))
    arrow_on((x0 + T, y0 + R), (x0 + T, y0), frac=0.35)
    arrow_on((x0 + T, y0), (x0, y0))


def plaquette(x0, i, j, y0=0.0):
    d = 0.17
    x, y = x0 + i + d, y0 + j + d
    w = 1 - 2 * d
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor=C_BLUE, alpha=0.12,
                               edgecolor="none"))
    ax.add_patch(plt.Rectangle((x, y), w, w, facecolor="none",
                               edgecolor=C_BLUE, lw=1.0, joinstyle="round"))
    arrow_on((x + w, y + w), (x, y + w), color=C_BLUE, ms=6)


def strips(x0, cols, y0=0.0):
    """Narrow vertical slits left after integrating columns in `cols`:
    the contour snakes up and down through those columns."""
    for i in cols:
        xa, xb = x0 + i + 0.33, x0 + i + 0.67
        ax.plot([xa, xa], [y0 + 0.12, y0 + R - 0.12], color=C_BLUE, lw=1.5)
        ax.plot([xb, xb], [y0 + 0.12, y0 + R - 0.12], color=C_BLUE, lw=1.5)
        # connect at the bottom to form a narrow U
        ax.plot([xa, xb], [y0 + 0.12, y0 + 0.12], color=C_BLUE, lw=1.5)
        arrow_on((xa, y0 + R - 0.12), (xa, y0 + 0.12), color=C_BLUE, ms=7)
        arrow_on((xb, y0 + 0.12), (xb, y0 + R - 0.12), color=C_BLUE, ms=7)


# ---- top row: successive integration of link columns -----------------------
X1, X2, X3, X4 = 0.0, 6.4, 12.8, 19.2
Y0 = 2.2

loop(X1, Y0)
for i in range(T):
    for j in range(R):
        plaquette(X1, i, j, Y0)
ax.text(X1 - 0.35, Y0 + R / 2, r"$\frac{1}{N}$", color=C_RED, ha="right",
        va="center", fontsize=10)

loop(X2, Y0)
strips(X2, [0], Y0)
for i in range(1, T):
    for j in range(R):
        plaquette(X2, i, j, Y0)

loop(X3, Y0)
strips(X3, [0, 1, 2], Y0)
for j in range(R):
    plaquette(X3, T - 1, j, Y0)

loop(X4, Y0)
strips(X4, range(T), Y0)
ax.text(X4 + T / 2, Y0 - 0.45, r"last trace $= N$", color=C_RED,
        ha="center", va="top", fontsize=9)

# arrows between panels with the accumulated factors
labels = [r"$\left(\frac{1}{N}\right)^{R}$", "",
          r"$\left(\frac{1}{N}\right)^{RT}$"]
for xa, lab in zip((X1 + T + 0.5, X2 + T + 0.5, X3 + T + 0.5), labels):
    ax.plot([xa, xa + 1.35], [Y0 + R / 2, Y0 + R / 2], color=C_GREEN, lw=1.3)
    arrow_on((xa, Y0 + R / 2), (xa + 1.4, Y0 + R / 2), color=C_GREEN,
             frac=1.0, ms=11)
    if lab:
        ax.text(xa + 0.7, Y0 + R / 2 - 0.35, lab, color=C_RED, ha="center",
                va="top", fontsize=9)

# ---- bottom: the merging identity ------------------------------------------
xb, yb = 0.6, 0.15
w = 0.9
# two plaquettes sharing the middle link U
ax.add_patch(plt.Rectangle((xb, yb), w, w, facecolor=C_BLUE, alpha=0.10,
                           edgecolor="none"))
ax.add_patch(plt.Rectangle((xb, yb), w, w, facecolor="none",
                           edgecolor=C_BLUE, lw=1.3, joinstyle="round"))
ax.add_patch(plt.Rectangle((xb, yb + w), w, w, facecolor=C_GREEN, alpha=0.10,
                           edgecolor="none"))
ax.add_patch(plt.Rectangle((xb, yb + w), w, w, facecolor="none",
                           edgecolor=C_GREEN, lw=1.3, joinstyle="round"))
arrow_on((xb, yb + w), (xb + w, yb + w), color=C_RED, ms=8)
ax.text(xb + w / 2, yb + 1.5 * w, r"$V$", color=C_GREEN, ha="center",
        va="center", fontsize=9)
ax.text(xb + w / 2, yb + 0.5 * w, r"$W$", color=C_BLUE, ha="center",
        va="center", fontsize=9)
ax.text(xb + w + 0.12, yb + w, r"$U$", color=C_RED, ha="left", va="center",
        fontsize=9)
# arrow to merged loop
ax.plot([xb + w + 1.1, xb + w + 2.1], [yb + w, yb + w], color=C_GREEN,
        lw=1.3)
arrow_on((xb + w + 1.1, yb + w), (xb + w + 2.15, yb + w), color=C_GREEN,
         frac=1.0, ms=11)
# merged tall loop tr[VW]
xm = xb + w + 2.7
ax.add_patch(plt.Rectangle((xm, yb), w, 2 * w, facecolor=C_BLUE, alpha=0.10,
                           edgecolor="none"))
ax.add_patch(plt.Rectangle((xm, yb), w, 2 * w, facecolor="none",
                           edgecolor=C_BLUE, lw=1.3, joinstyle="round"))
ax.text(xm + w + 0.7, yb + w,
        r"$\int \mathrm{d}U\,\mathrm{tr}[VU^{\dagger}]\,"
        r"\mathrm{tr}[UW]=\frac{1}{N}\,\mathrm{tr}[VW]$",
        color=C_RED, ha="left", va="center", fontsize=10)

ax.set_xlim(-1.0, X4 + T + 0.4)
ax.set_ylim(-0.15, Y0 + R + 0.35)

fig.savefig("../fig-redraw-058.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-058.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 058")

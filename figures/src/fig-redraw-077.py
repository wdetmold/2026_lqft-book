"""Redraw of fig-notes-077: the overlap operator maps the spectrum of its
kernel -- the Wilson operator at m = 0, whose spectral region (in units of
1/a) touches the real axis with cusps at the doubler points 0,2,4,6,8 --
onto the Ginsparg-Wilson circle of radius 1/a through the origin."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrow

BLUE = "#0072B2"
GREEN = "#009E73"
LGREEN = "#d6ecd9"
ORANGE = "#D55E00"

fig = plt.figure(figsize=(7.4, 3.1))
gs = fig.add_gridspec(1, 3, width_ratios=[1.55, 0.34, 1.05], wspace=0.06)
axL = fig.add_subplot(gs[0])
axM = fig.add_subplot(gs[1])
axR = fig.add_subplot(gs[2])
for a in (axL, axM, axR):
    a.set_aspect("equal")
    a.axis("off")

# ---- left: spectrum of the Wilson kernel at m = 0 -------------------------
axL.add_patch(Ellipse((4, 0), 8, 6.4, facecolor=LGREEN, edgecolor=BLUE,
                      lw=1.2, zorder=1))
for c in (1, 3, 5, 7):  # cusps at the doubler points: white circular bites
    axL.add_patch(Circle((c, 0), 1, facecolor="white", edgecolor=BLUE,
                         lw=1.1, zorder=2))

# real eigenvalues along the axis
xs = np.linspace(0.25, 7.75, 26)
axL.plot(xs, 0 * xs, ls="none", marker="o", ms=2.2, color=GREEN, zorder=4)

# axes as arrows through the origin
axL.annotate("", xy=(9.4, 0), xytext=(-1.0, 0),
             arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                             mutation_scale=12), zorder=3)
axL.annotate("", xy=(0, 4.0), xytext=(0, -3.7),
             arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                             mutation_scale=12), zorder=3)
axL.text(9.55, -0.35, r"$\mathrm{Re}\,a\lambda$", ha="left", va="top",
         fontsize=10)
axL.text(0.25, 3.85, r"$\mathrm{Im}\,a\lambda$", ha="left", va="top",
         fontsize=10)
for c in (2, 4, 6, 8):
    axL.text(c, -0.42, rf"${c}$", ha="center", va="top", fontsize=9,
             zorder=4)

axL.text(4, -4.35, "spectrum of $D_{\\mathrm{Wilson}}$ ($m=0$):\n"
         "cusps related to doubler modes",
         ha="center", va="top", fontsize=9)
axL.set_xlim(-1.4, 11.3)
axL.set_ylim(-5.9, 4.4)

# ---- middle: mapping arrow ------------------------------------------------
axM.add_patch(FancyArrow(0.02, 0.5, 0.93, 0, width=0.16, head_width=0.42,
                         head_length=0.32, length_includes_head=True,
                         facecolor=LGREEN, edgecolor=GREEN, lw=1.2))
axM.set_xlim(0, 1)
axM.set_ylim(0, 1)

# ---- right: the Ginsparg-Wilson circle ------------------------------------
axR.annotate("", xy=(3.4, 0), xytext=(-1.45, 0),
             arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                             mutation_scale=12))
axR.annotate("", xy=(0, 1.75), xytext=(0, -1.75),
             arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                             mutation_scale=12))
axR.text(3.4, -0.18, r"$\mathrm{Re}\,\lambda$", ha="right", va="top",
         fontsize=10)
axR.text(0.12, 1.70, r"$\mathrm{Im}\,\lambda$", ha="left", va="top",
         fontsize=10)

th = np.linspace(0, 2 * np.pi, 400)
axR.plot(1 + np.cos(th), np.sin(th), color=BLUE, lw=1.8, zorder=3)
axR.plot([1], [0], marker="o", ms=4, color=BLUE, zorder=4)
axR.text(1.02, -0.16, r"$\frac{1}{a}$", color=BLUE, ha="center", va="top",
         fontsize=11)
phi = np.deg2rad(52)
axR.annotate("", xy=(1 + np.cos(phi), np.sin(phi)), xytext=(1, 0),
             arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.3,
                             mutation_scale=11))
axR.text(1 + 0.58 * np.cos(phi) - 0.10, 0.58 * np.sin(phi) + 0.05,
         r"$\frac{1}{a}$", color=BLUE, ha="right", va="bottom", fontsize=11)

axR.plot([2], [0], marker="o", ms=5, color=ORANGE, zorder=4)
axR.annotate("doubler modes\nall live here",
             xy=(2.05, -0.12), xytext=(2.75, -1.35),
             color=ORANGE, fontsize=9, ha="center", va="top",
             arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1,
                             connectionstyle="arc3,rad=-0.35",
                             mutation_scale=11))

axR.set_xlim(-1.6, 3.6)
axR.set_ylim(-2.4, 1.9)

fig.savefig("../fig-redraw-077.pdf")
fig.savefig("../fig-redraw-077.png", dpi=200)
print("done 077")

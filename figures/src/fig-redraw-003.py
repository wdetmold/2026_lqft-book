"""Redraw of fig-notes-003: schematic phase diagram of the O(n) model.

Left: (lambda, kappa) plane. Critical line kappa_c(lambda) runs from 1/8 at
lambda = 0 to 0.07475... (4d Ising) at lambda = infinity; mirror line at
negative kappa (kappa -> -kappa symmetry). Symmetric phase between the lines,
broken (= Higgs) phase outside. Right: equivalent (lambda_0, m_0^2) plane,
with the boundary descending from the origin; the lambda_0 = 0, m_0^2 < 0
axis is nonsensical (unbounded action).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

C_CURVE = "#0072B2"   # phase boundaries
C_REG = "#009E73"     # phase labels
C_ANN = "#D55E00"     # annotations

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.3))
fig.subplots_adjust(wspace=0.42)

# ---- left panel: (lambda, kappa) plane, x in [0,1] maps lambda = 0..inf ---
x = np.linspace(0.0, 1.0, 300)
kc = PchipInterpolator(
    [0.00, 0.15, 0.35, 0.55, 0.75, 0.90, 1.00],
    [0.125, 0.141, 0.150, 0.145, 0.121, 0.094, 0.07475])
axL.plot(x, kc(x), color=C_CURVE, lw=1.8, zorder=3)
axL.plot(x, -kc(x), color=C_CURVE, lw=1.8, zorder=3)
axL.axhline(0.0, color="0.35", lw=0.9, ls=(0, (5, 4)), zorder=1)
axL.axvline(1.0, color="0.55", lw=0.8, zorder=1)

# phase labels
axL.text(0.42, 0.20, r"broken $=$ Higgs", color=C_REG, ha="center",
         va="center", fontsize=10)
axL.text(0.42, 0.055, "symmetric", color=C_REG, ha="center",
         va="center", fontsize=10)
axL.text(0.42, -0.20, r"broken $=$ Higgs", color=C_REG, ha="center",
         va="center", fontsize=10)

# endpoint value at lambda = infinity (4d Ising)
axL.annotate("$0.07475\\ldots$\n(4d Ising)", xy=(1.0, 0.07475),
             xytext=(0.80, 0.242), color=C_ANN, fontsize=9,
             ha="center", va="center",
             arrowprops=dict(arrowstyle="-|>", color=C_ANN, lw=0.9,
                             shrinkA=2, shrinkB=2))
# lambda = infinity boundary is the Ising model
axL.annotate("Ising model", xy=(0.995, -0.30), xytext=(0.80, -0.24),
             color=C_ANN, fontsize=9, ha="right", va="center",
             annotation_clip=False,
             arrowprops=dict(arrowstyle="-|>", color=C_ANN, lw=0.9,
                             shrinkA=2, shrinkB=2))
# kappa -> -kappa symmetry note
axL.text(0.02, -0.315,
         r"$\kappa\to-\kappa$ related by $\phi_n\to(-1)^{\sum_i n_i}\phi_n$",
         color=C_ANN, fontsize=8, ha="left", va="center")

axL.set_xlim(0, 1)
axL.set_ylim(-0.34, 0.31)
axL.set_xticks([0, 1])
axL.set_xticklabels(["$0$", r"$\infty$"])
axL.set_yticks([0, 0.125])
axL.set_yticklabels(["$0$", r"$\frac{1}{8}$"])
axL.set_xlabel(r"$\lambda$")
axL.set_ylabel(r"$\kappa$", rotation=0, labelpad=8)
axL.minorticks_off()
axL.tick_params(length=0)
for s in ("top", "right"):
    axL.spines[s].set_visible(False)

# ---- right panel: (lambda_0, m_0^2) plane, x in [0,1] maps 0..inf --------
xr = np.linspace(0.0, 1.0, 300)
bc = PchipInterpolator(
    [0.00, 0.12, 0.30, 0.55, 0.80, 1.00],
    [0.00, -0.30, -0.53, -0.71, -0.82, -0.90])
axR.plot(xr, bc(xr), color=C_CURVE, lw=1.6, zorder=3)

axR.text(0.70, -0.28, "symmetric", color=C_REG, ha="center",
         va="center", fontsize=10)
axR.text(0.58, -0.87, r"broken $=$ Higgs", color=C_REG, ha="center",
         va="center", fontsize=10)

# lambda_0 = 0, m_0^2 < 0 axis is nonsensical (unbounded action)
axR.plot([0.0, 0.0], [-0.02, -0.42], color=C_ANN, lw=1.8,
         ls=(0, (2.2, 2.2)), zorder=4, clip_on=False)
axR.annotate("$\\lambda_0=0,\\ m_0^2<0$\nnonsensical",
             xy=(0.015, -0.35), xytext=(0.10, -0.72), color=C_ANN,
             fontsize=9, ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color=C_ANN, lw=0.9,
                             shrinkA=2, shrinkB=2))

axR.set_xlim(0, 1)
axR.set_ylim(-1.0, 0.0)
axR.set_xticks([0, 1])
axR.set_xticklabels(["$0$", r"$\infty$"])
axR.set_yticks([0])
axR.set_yticklabels(["$0$"])
axR.set_xlabel(r"$\lambda_0$")
axR.xaxis.set_label_position("top")
axR.xaxis.tick_top()
axR.set_ylabel(r"$m_0^2$", rotation=0)
axR.yaxis.set_label_coords(-0.08, 0.88)
axR.minorticks_off()
axR.tick_params(length=0, labelbottom=False, labeltop=True)
for s in ("bottom", "right"):
    axR.spines[s].set_visible(False)

# equivalence arrow between the two parametrisations
mid = 0.5 * (axL.get_position().x1 + axR.get_position().x0)
fig.text(mid, 0.5, r"$\Longleftrightarrow$", ha="center", va="center",
         fontsize=17)

fig.savefig("../fig-redraw-003.pdf")
fig.savefig("../fig-redraw-003.png", dpi=200)

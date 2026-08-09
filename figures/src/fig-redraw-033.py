"""Redraw of fig-notes-033: loss of physical information for K -> pi pi
in infinite volume (scattering continuum masks the state) and in finite
volume (discrete two-pion levels whose kinematics do not match m_K except
for very particular volumes)."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_BLUE = "#0072B2"
C_GREEN = "#009E73"

M_PI = 0.5
DP = 0.45  # (2*pi/L) in sketch units
levels = [2.0 * np.sqrt(M_PI**2 + n * DP**2) for n in range(4)]  # 1.0 ... 1.84
M_K = 1.5

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(6.4, 3.0), gridspec_kw=dict(width_ratios=[1.0, 1.55]))

for ax in (axL, axR):
    ax.set_xlim(-1.15, 1.7)
    ax.set_ylim(0.0, 2.35)
    ax.axis("off")
    # vertical energy axis with arrow head
    ax.annotate("", xy=(0, 2.28), xytext=(0, 0.0),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                                shrinkA=0, shrinkB=0))
    ax.text(-0.16, 2.2, r"$E$", ha="right", va="center", fontsize=12)
    # m_K arrow pointing left away from the axis
    ax.annotate("", xy=(-0.8, M_K), xytext=(0, M_K),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.text(-0.88, M_K, r"$m_K$", ha="right", va="center",
            color=C_RED, fontsize=10)

# ---- left panel: infinite volume ----
axL.set_title("infinite volume", fontsize=10, pad=4)
# scattering continuum above 2 m_pi
axL.add_patch(plt.Rectangle((0.0, levels[0]), 0.85, 2.05 - levels[0],
                            facecolor="0.88", edgecolor="none", zorder=0))
axL.annotate("", xy=(1.05, levels[0]), xytext=(0, levels[0]),
             arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.6,
                             shrinkA=0, shrinkB=0))
axL.text(1.13, levels[0], r"$2m_\pi$", ha="left", va="center",
         color=C_BLUE, fontsize=10)
axL.text(0.95, 1.82, "scattering\ncontinuum", ha="left", va="center",
         fontsize=8.5, color="0.35")

# ---- right panel: finite volume ----
axR.set_xlim(-1.15, 3.4)
axR.set_title("finite volume", fontsize=10, pad=4)
lab = [r"$2m_\pi$",
       r"$2\sqrt{m_\pi^2 + (2\pi/L)^2}$",
       r"$2\sqrt{m_\pi^2 + 2(2\pi/L)^2}$",
       r"$2\sqrt{m_\pi^2 + 3(2\pi/L)^2}$"]
for E, s in zip(levels, lab):
    axR.annotate("", xy=(1.0, E), xytext=(0, E),
                 arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.6,
                                 shrinkA=0, shrinkB=0))
    axR.text(1.1, E, s, ha="left", va="center", color=C_BLUE, fontsize=8.5)
axR.text(1.35, 0.52, "kinematics do not match\nexcept for very\nparticular volumes",
         ha="left", va="top", color=C_GREEN, fontsize=8.5, style="italic")

fig.savefig("../fig-redraw-033.pdf")
fig.savefig("../fig-redraw-033.png", dpi=200)

"""Book-style redraw of FIG. 41: QCD thermodynamic observables vs temperature.

Schematic recreation (shapes after HotQCD/Budapest-Wuppertal EoS results) of the
hand-drawn lecture figure. Demonstrates the agentic redraw workflow: semantic
recreation from a house stylesheet, not pixel tracing.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# ---- house style (would live in a shared lqftbook.mplstyle) ----------------
plt.style.use("lqftbook.mplstyle")
_unused = ({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 11,
    "axes.linewidth": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "figure.dpi": 200,
})

C_TRACE = "#D55E00"   # vermillion  — (eps-3p)/T^4
C_ENTR  = "#0072B2"   # blue        — s/4T^3
C_PRESS = "#009E73"   # green       — p/T^4
C_YM    = "#CC79A7"   # purple      — p/T^4 in SU(3) YM
C_HRG   = "#444444"   # gray dashed — hadron resonance gas
C_SB    = "#888888"   # dotted      — Stefan-Boltzmann limit

T = np.linspace(130, 400, 400)

def curve(pts):
    x, y = zip(*pts)
    return PchipInterpolator(x, y)(np.clip(T, x[0], x[-1])), x

trace, _ = curve([(130, 1.20), (150, 2.20), (170, 3.30), (195, 4.05),
                  (220, 3.90), (250, 3.30), (300, 2.55), (350, 2.00), (400, 1.65)])
entr, _  = curve([(130, 0.60), (150, 0.95), (170, 1.60), (200, 2.45),
                  (250, 3.25), (300, 3.70), (350, 3.95), (400, 4.10)])
press, _ = curve([(130, 0.55), (150, 0.80), (170, 1.20), (200, 1.75),
                  (250, 2.45), (300, 2.90), (350, 3.20), (400, 3.40)])

T_hrg = np.linspace(130, 172, 60)
hrg = PchipInterpolator([130, 145, 160, 172], [1.10, 1.70, 2.55, 3.30])(T_hrg)

T_ym = np.linspace(262, 400, 100)
ym = PchipInterpolator([262, 270, 285, 320, 360, 400],
                       [0.00, 0.12, 0.55, 1.00, 1.30, 1.50])(T_ym)

fig, ax = plt.subplots(figsize=(5.2, 3.6))

ax.axhline(5.21, color=C_SB, lw=1.0, ls=":", zorder=1)
ax.text(396, 5.05, "Stefan–Boltzmann limit", color="#666666",
        ha="right", va="top", fontsize=9)

ax.plot(T, trace, color=C_TRACE, lw=1.8, zorder=3)
ax.plot(T, entr, color=C_ENTR, lw=1.8, zorder=3)
ax.plot(T, press, color=C_PRESS, lw=1.8, zorder=3)
ax.plot(T_hrg, hrg, color=C_HRG, lw=1.4, ls="--", zorder=2)
ax.plot(T_ym, ym, color=C_YM, lw=1.8, ls="-.", zorder=3)

ax.text(207, 4.22, r"$(\varepsilon - 3p)/T^4$", color=C_TRACE, fontsize=11)
ax.text(352, 4.25, r"$s/4T^3$", color=C_ENTR, fontsize=11)
ax.text(355, 3.02, r"$p/T^4$", color=C_PRESS, fontsize=11)
ax.text(151, 2.62, "HRG", color=C_HRG, fontsize=9, rotation=52)
ax.text(322, 0.62, r"$p/T^4$, $SU(3)$ YM", color=C_YM, fontsize=9.5)

ax.set_xlim(130, 400)
ax.set_ylim(0, 5.6)
ax.set_xlabel(r"$T\ \mathrm{[MeV]}$")
ax.set_ylabel(r"$(\varepsilon-3p)/T^4,\ \ s/4T^3,\ \ p/T^4$")
ax.set_xticks([150, 200, 250, 300, 350, 400])

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-024.pdf")
fig.savefig("../fig-redraw-024.png", dpi=220)
print("done")

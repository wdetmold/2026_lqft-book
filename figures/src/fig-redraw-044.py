"""Redraw of fig-notes-044: expected RG flow for YM theory in coupling space.

Perspective view of the space {1/beta, kappa_1, kappa_2, ...}: the critical
surface at beta = infinity (shaded plane spanned by kappa_1, kappa_2)
contains the fixed point {beta = infinity, kappa*}, to which flow within the
surface is attracted (green arrows). The renormalised trajectory (blue)
leaves the FP perpendicular to the surface; a trajectory started at a
generic point {beta < infinity, kappa} (purple) is drawn towards the FP and
then flows out along the RT. The red dotted line FP(beta, kappa*) marks the
FP action at finite beta.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

CGREEN = "#009E73"
CBLUE = "#0072B2"
CRED = "#D55E00"
CPURP = "#7B52A1"

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# Projection unit vectors: e1 = kappa_1 (into page, down-left), e2 = kappa_2 (up).
e1 = np.array([-0.75, -0.68])
e2 = np.array([0.0, 1.0])

def P(u, v):
    return u * e1 + v * e2

# Critical surface (beta = infinity): parallelogram in the kappa_1-kappa_2 plane.
corners = np.array([P(-0.2, -0.3), P(1.7, -0.3), P(1.7, 2.1), P(-0.2, 2.1)])
ax.add_patch(plt.Polygon(corners, closed=True, facecolor=CGREEN, alpha=0.18,
                         edgecolor="none", zorder=0))
ax.text(-1.72, -0.62, "critical surface\n" + r"$(\beta = \infty)$",
        color=CGREEN, fontsize=9.5, ha="center", va="top")

# Axes (drawn over the surface).
axprops = dict(arrowstyle="-|>,head_width=0.16,head_length=0.32",
               color=CGREEN, lw=1.4, shrinkA=0, shrinkB=0)
O = np.array([0.0, 0.0])
ax.annotate("", xy=(0, 2.25), xytext=O, arrowprops=axprops, zorder=2)
ax.annotate("", xy=(3.95, 0.30), xytext=O, arrowprops=axprops, zorder=2)
ax.annotate("", xy=tuple(P(2.0, 0.0)), xytext=O, arrowprops=axprops, zorder=2)
ax.text(0.10, 2.22, r"$\kappa_2$", color=CGREEN, fontsize=12, ha="left")
ax.text(3.95, 0.12, r"$1/\beta$", color=CGREEN, fontsize=12, ha="right", va="top")
ax.text(*(P(2.0, 0.0) + [-0.02, -0.10]), r"$\kappa_1$", color=CGREEN,
        fontsize=12, ha="right", va="top")

# Fixed point on the critical surface.
FP = P(0.9, 1.35)
ax.plot(*FP, "o", ms=6, color=CBLUE, zorder=6)
ax.text(FP[0] - 0.12, FP[1] + 0.30, r"$\{\beta = \infty,\ \kappa^*\}$",
        color=CBLUE, fontsize=10, ha="right", va="bottom")

# Flow within the critical surface: arrows attracted towards the FP.
flowprops = dict(arrowstyle="-|>,head_width=0.14,head_length=0.28",
                 color=CGREEN, lw=1.2, shrinkA=0, shrinkB=0)
for (u0, v0) in [(0.25, 0.55), (0.35, 1.85), (1.45, 0.70),
                 (1.5, 1.9), (0.2, 1.25), (1.55, 1.3)]:
    p0 = P(u0, v0)
    p1 = p0 + 0.42 * (FP - p0) / np.linalg.norm(FP - p0)
    ax.annotate("", xy=tuple(p1), xytext=tuple(p0), arrowprops=flowprops, zorder=1)

def curve(pts, n=300):
    pts = np.asarray(pts, float)
    t = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    tt = np.linspace(0, t[-1], n)
    return PchipInterpolator(t, pts[:, 0])(tt), PchipInterpolator(t, pts[:, 1])(tt)

def flow_arrows(x, y, fracs, color):
    props = dict(arrowstyle="-|>,head_width=0.16,head_length=0.32",
                 color=color, lw=0, shrinkA=0, shrinkB=0)
    for f in fracs:
        i = int(f * (len(x) - 1))
        ax.annotate("", xy=(x[i + 1], y[i + 1]), xytext=(x[i], y[i]),
                    arrowprops=props, zorder=5)

# Renormalised trajectory: leaves the FP perpendicular to the surface.
xr, yr = curve([FP, (0.2, 0.82), (1.2, 1.06), (2.4, 1.44), (3.45, 1.64)])
ax.plot(xr, yr, color=CBLUE, lw=1.8, zorder=4)
flow_arrows(xr, yr, [0.30, 0.60, 0.88], CBLUE)
ax.text(3.55, 1.64, "renormalised\ntrajectory", color=CBLUE, fontsize=10,
        ha="left", va="center")

# Trajectory from a generic starting point {beta < infinity, kappa}.
S = np.array([0.32, 1.80])
xp, yp = curve([S, (-0.20, 1.60), (-0.58, 1.22), FP + [0.03, 0.10],
                (0.25, 0.92), (1.25, 1.14), (2.45, 1.52), (3.3, 1.70)])
ax.plot(xp, yp, color=CPURP, lw=1.6, zorder=3)
flow_arrows(xp, yp, [0.12, 0.35, 0.62, 0.85], CPURP)
ax.plot(*S, "o", ms=5, color=CPURP, zorder=6)
ax.text(S[0] + 0.10, S[1] + 0.05, r"$\{\beta < \infty,\ \kappa\}$",
        color=CPURP, fontsize=10, ha="left", va="bottom")

# FP action at finite beta: dotted line kappa = kappa* away from the surface.
ax.plot([FP[0], 2.55], [FP[1], FP[1]], color=CRED, lw=1.4, ls=":", zorder=2)
ax.text(2.65, FP[1], r"FP$(\beta, \kappa^*)$", color=CRED, fontsize=10,
        ha="left", va="center")

ax.set_xlim(-2.5, 4.6)
ax.set_ylim(-1.6, 2.5)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-044.pdf")
fig.savefig("../fig-redraw-044.png", dpi=200)
print("done")

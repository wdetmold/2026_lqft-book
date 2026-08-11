"""Redraw of fig-notes-046: Schroedinger-functional correlation functions on
the space-time cylinder with boundary gauge fields C (t=0) and C' (t=T).
Left: f_P(x_0) -- boundary sources at t=0 joined to a pseudoscalar insertion
on the time slice x_0 (dashed).  Right: f_1 -- boundary-to-boundary
correlator running from t=0 to t=T."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Ellipse

BLUE = "#0072B2"
LBLUE = "#dbe9f6"
ORANGE = "#D55E00"

W, H = 2.2, 2.4       # cylinder width and height
RY = 0.34             # cap ellipse semi-minor full height


def cylinder(ax, cx):
    y0, y1 = 0.0, H
    # walls
    for s in (-1, 1):
        ax.plot([cx + s * W / 2, cx + s * W / 2], [y0, y1],
                color=BLUE, lw=1.6, zorder=2)
    # caps (t = 0 and t = T boundaries)
    for y in (y0, y1):
        ax.add_patch(Ellipse((cx, y), W, RY, facecolor=LBLUE,
                             edgecolor=BLUE, lw=1.6, zorder=3))
    # labels
    ax.text(cx - W / 2 - 0.22, y1, r"$T$", ha="right", va="center",
            fontsize=13)
    ax.text(cx - W / 2 - 0.22, y0, r"$0$", ha="right", va="center",
            fontsize=13)
    ax.text(cx + W / 2 + 0.14, y1 + 0.18, r"$C^{\prime}$", ha="left",
            va="center", fontsize=13)
    ax.text(cx + W / 2 + 0.14, y0 - 0.18, r"$C$", ha="left", va="center",
            fontsize=13)


def wiggly(ax, p0, p1, amp=0.055, waves=1.5):
    """gently wavy quark line from p0 to p1"""
    t = np.linspace(0, 1, 120)
    x = p0[0] + (p1[0] - p0[0]) * t + amp * np.sin(waves * 2 * np.pi * t)
    y = p0[1] + (p1[1] - p0[1]) * t
    ax.plot(x, y, color=ORANGE, lw=1.9, solid_capstyle="round", zorder=4)


fig, ax = plt.subplots(figsize=(6.4, 2.6))
ax.set_aspect("equal")
ax.axis("off")

# ---- left: f_P(x_0) -------------------------------------------------------
cx = 0.0
cylinder(ax, cx)
x0h = 0.62 * H
# dashed time-slice at x_0
ax.add_patch(Ellipse((cx, x0h), 1.07 * W, 1.25 * RY, fill=False,
                     edgecolor=ORANGE, lw=0.9, ls=(0, (3, 3)), zorder=1))
ax.text(cx - W / 2 - 0.22, x0h, r"$x_0$", ha="right", va="center",
        fontsize=13)
# boundary sources joined at the operator insertion
a = (cx - 0.36 * W, -0.06)
b = (cx + 0.26 * W, -0.09)
top = (cx - 0.03 * W, x0h + 0.05)
wiggly(ax, a, top)
wiggly(ax, b, top)
for p in (a, b):
    ax.plot([p[0]], [p[1]], marker="o", ms=6.5, color=ORANGE, zorder=5)
ax.plot([top[0]], [top[1]], marker="o", ms=6, color=ORANGE, zorder=5)
ax.text(cx, -0.72, r"$f_P(x_0)$", ha="center", va="top", fontsize=12)

# ---- right: f_1 -----------------------------------------------------------
cx = 4.6
cylinder(ax, cx)
pairs = [((cx - 0.28 * W, -0.06), (cx - 0.12 * W, H + 0.05)),
         ((cx + 0.28 * W, -0.08), (cx + 0.33 * W, H + 0.03))]
for p0, p1 in pairs:
    wiggly(ax, p0, p1, amp=0.05, waves=1.2)
    for p in (p0, p1):
        ax.plot([p[0]], [p[1]], marker="o", ms=6.5, color=ORANGE, zorder=5)
ax.text(cx, -0.72, r"$f_1$", ha="center", va="top", fontsize=12)

ax.set_xlim(-2.1, 6.8)
ax.set_ylim(-1.25, H + 0.6)

fig.savefig("../fig-redraw-046.pdf")
fig.savefig("../fig-redraw-046.png", dpi=200)

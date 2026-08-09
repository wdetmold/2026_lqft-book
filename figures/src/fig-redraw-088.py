"""Redraw of fig-notes-088: Dirac-operator eigenvalue spectrum in the
complex lambda plane (fixed-point / Ginsparg-Wilson action).

Both circles pass through the origin with centres on the real axis, as in
the sketch: the large (Ginsparg-Wilson) circle and a smaller circle nested
inside it, tangent at lambda = 0.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

CRED = "#D55E00"

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# Large eigenvalue circle through the origin, centred on the real axis.
ax.add_patch(plt.Circle((1.0, 0.0), 1.0, facecolor=CRED, alpha=0.15,
                        edgecolor=CRED, lw=1.8, zorder=2))
# Smaller circle through the origin, nested inside the large one.
ax.add_patch(plt.Circle((0.28, 0.0), 0.28, facecolor="white",
                        edgecolor=CRED, lw=1.8, zorder=3))

# Complex-plane axes through the origin.
axprops = dict(arrowstyle="-|>,head_width=0.16,head_length=0.32",
               color="black", lw=1.0, shrinkA=0, shrinkB=0)
ax.annotate("", xy=(2.65, 0.0), xytext=(-0.45, 0.0), arrowprops=axprops, zorder=4)
ax.annotate("", xy=(0.0, 1.35), xytext=(0.0, -1.35), arrowprops=axprops, zorder=1)
ax.text(2.62, -0.10, r"Re$\,\lambda$", fontsize=11, ha="right", va="top")
ax.text(0.07, 1.32, r"Im$\,\lambda$", fontsize=11, ha="left", va="top")

ax.set_xlim(-0.55, 2.75)
ax.set_ylim(-1.45, 1.45)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-088.pdf")
fig.savefig("../fig-redraw-088.png", dpi=200)
print("done")

"""Redraw of fig-notes-012: gauge transformation Omega(n) acting on a single
site n, modifying the 2D links that touch it; choosing Omega(n) = U_nu^dag(n)
sets the outgoing nu-link to unity.

Note: the sketch writes Omega(n) (no dagger) on the incoming links; here we
use the convention of the surrounding text, U_mu(n) -> Omega(n) U_mu(n)
Omega^dag(n + mu-hat), so incoming links pick up Omega^dag(n) on the right.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

from matplotlib.patches import FancyArrowPatch

C_RED = "#D55E00"    # gauge-transform factors / transformed pieces
C_BLUE = "#0072B2"   # original link variables
C_GREEN = "#009E73"  # lattice links

fig, ax = plt.subplots(figsize=(9.6, 2.6))
ax.set_aspect("equal")
ax.axis("off")

A = 1.3   # arm length of each cross
FS = 10


def cross(cx):
    """Draw the 2D cross of links around site n."""
    ax.plot([cx - A, cx + A], [0, 0], color=C_GREEN, lw=1.8, zorder=1)
    ax.plot([cx, cx], [-A, A], color=C_GREEN, lw=1.8, zorder=1)
    ax.plot([cx], [0], marker="o", ms=5.5, color=C_BLUE, zorder=3)
    # direction arrowheads (all links oriented in +mu / +nu direction)
    for (x0, y0, x1, y1) in [(cx + 0.55, 0, cx + 0.80, 0),      # U_mu(n)
                             (cx, 0.55, cx, 0.80),              # U_nu(n)
                             (cx - 0.80, 0, cx - 0.55, 0),      # U_mu(n-mu)
                             (cx, -0.80, cx, -0.55)]:           # U_nu(n-nu)
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color=C_GREEN, lw=1.8, zorder=2))


def duo(x, y, s1, c1, s2, c2, va="bottom"):
    """Two-colour label: s1 ends at (x, y), s2 starts there."""
    ax.text(x, y, s1, color=c1, ha="right", va=va, fontsize=FS)
    ax.text(x, y, s2, color=c2, ha="left", va=va, fontsize=FS)


# ---- panel 1: original links ----------------------------------------------
c1 = 0.0
cross(c1)
ax.text(c1 + 0.20, 0.18, r"$U_\mu(n)$", color=C_BLUE, ha="left",
        va="bottom", fontsize=FS)
ax.text(c1 + 0.16, 1.02, r"$U_\nu(n)$", color=C_BLUE, ha="left",
        va="center", fontsize=FS)
ax.text(c1 - 0.20, 0.18, r"$U_\mu(n-\hat{\mu})$", color=C_BLUE, ha="right",
        va="bottom", fontsize=FS)
ax.text(c1 + 0.16, -1.02, r"$U_\nu(n-\hat{\nu})$", color=C_BLUE, ha="left",
        va="center", fontsize=FS)
ax.text(c1 - 0.18, -0.26, r"$n$", color=C_BLUE, ha="right", va="top",
        fontsize=FS)

# ---- panel 2: after a gauge transformation Omega(n) at site n --------------
c2 = 7.6
cross(c2)
duo(c2 + 1.00, 0.18, r"$\Omega(n)\,$", C_RED, r"$U_\mu(n)$", C_BLUE)
duo(c2 + 0.95, 1.02, r"$\Omega(n)\,$", C_RED, r"$U_\nu(n)$", C_BLUE,
    va="center")
duo(c2 - 1.15, 0.18, r"$U_\mu(n-\hat{\mu})$", C_BLUE,
    r"$\,\Omega^{\dagger}(n)$", C_RED)
duo(c2 + 1.75, -1.02, r"$U_\nu(n-\hat{\nu})$", C_BLUE,
    r"$\,\Omega^{\dagger}(n)$", C_RED, va="center")

# ---- panel 3: the choice Omega(n) = U_nu^dag(n) ----------------------------
c3 = 15.6
cross(c3)
duo(c3 + 1.20, 0.18, r"$U_\nu^{\dagger}(n)\,$", C_RED, r"$U_\mu(n)$", C_BLUE)
ax.text(c3 + 0.18, 1.02, r"$1$", color=C_RED, ha="left", va="center",
        fontsize=FS + 1)
duo(c3 - 0.95, 0.18, r"$U_\mu(n-\hat{\mu})$", C_BLUE, r"$\,U_\nu(n)$", C_RED)
duo(c3 + 1.75, -1.02, r"$U_\nu(n-\hat{\nu})$", C_BLUE, r"$\,U_\nu(n)$",
    C_RED, va="center")

# ---- arrows between panels -------------------------------------------------
for (x0, x1, lab) in [(2.75, 4.65, r"$\Omega(n)$"),
                      (10.65, 12.65, r"$\Omega(n) = U_\nu^{\dagger}(n)$")]:
    ax.add_patch(FancyArrowPatch((x0, 0), (x1, 0), arrowstyle="-|>",
                                 mutation_scale=15, color=C_GREEN, lw=1.8))
    ax.text(0.5 * (x0 + x1), -0.30, lab, color=C_RED, ha="center",
            va="top", fontsize=FS)

ax.set_xlim(-2.0, 18.5)
ax.set_ylim(-1.8, 1.7)

fig.savefig("../fig-redraw-012.pdf")
fig.savefig("../fig-redraw-012.png", dpi=200)
print("done 012")

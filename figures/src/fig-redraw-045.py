"""Redraw of fig-notes-045: degrees of freedom of the lattice SUSY theory.

One plaquette of the 2d lattice. Site fields eta at n; link fields
(U_mu, psi_mu) oriented n -> n+mu and Ubar_mu oriented n+mu -> n (and
likewise in the nu direction); diagonal fields F_munu oriented
n -> n+mu+nu and chi_munu oriented n+mu+nu -> n.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

CBLUE = "#0072B2"
CRED = "#D55E00"
CGREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 3.4))

# Plaquette and diagonal.
ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=CBLUE, lw=1.8, zorder=2)
ax.plot([0, 1], [0, 1], color=CGREEN, lw=1.8, zorder=1)
for x, y in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    ax.plot(x, y, "o", ms=5, color=CBLUE, zorder=3)

# Site labels.
ax.text(-0.04, -0.10, r"$n$", color=CBLUE, fontsize=11, ha="right", va="top")
ax.text(1.05, -0.10, r"$n+\hat{\mu}$", color=CBLUE, fontsize=11, ha="left", va="top")
ax.text(-0.05, 1.08, r"$n+\hat{\nu}$", color=CBLUE, fontsize=11, ha="right")
ax.text(1.05, 1.08, r"$n+\hat{\mu}+\hat{\nu}$", color=CBLUE, fontsize=11, ha="left")

# Site field eta at n.
ax.text(-0.17, -0.02, r"$\eta$", color=CRED, fontsize=13, ha="right", va="center")

arrow = dict(arrowstyle="-|>,head_width=0.18,head_length=0.36",
             color=CRED, lw=1.5, shrinkA=0, shrinkB=0)

# Bottom edge: U_mu, psi_mu forward; Ubar_mu backward.
ax.annotate("", xy=(0.92, -0.12), xytext=(0.58, -0.12), arrowprops=arrow)
ax.text(0.75, -0.19, r"$\mathcal{U}_\mu,\ \psi_\mu$", color=CRED,
        fontsize=12, ha="center", va="top")
ax.annotate("", xy=(0.10, -0.12), xytext=(0.44, -0.12), arrowprops=arrow)
ax.text(0.27, -0.19, r"$\bar{\mathcal{U}}_\mu$", color=CRED,
        fontsize=12, ha="center", va="top")

# Left edge: U_nu, psi_nu upward; Ubar_nu downward.
ax.annotate("", xy=(-0.12, 0.92), xytext=(-0.12, 0.58), arrowprops=arrow)
ax.text(-0.19, 0.75, r"$\mathcal{U}_\nu,\ \psi_\nu$", color=CRED,
        fontsize=12, ha="right", va="center")
ax.annotate("", xy=(-0.12, 0.10), xytext=(-0.12, 0.44), arrowprops=arrow)
ax.text(-0.19, 0.27, r"$\bar{\mathcal{U}}_\nu$", color=CRED,
        fontsize=12, ha="right", va="center")

# Diagonal: F_munu towards n+mu+nu, chi_munu towards n.
ax.annotate("", xy=(0.90, 0.82), xytext=(0.68, 0.60), arrowprops=arrow)
ax.text(0.72, 0.80, r"$\mathcal{F}_{\mu\nu}$", color=CRED,
        fontsize=12, ha="right", va="bottom")
ax.annotate("", xy=(0.18, 0.10), xytext=(0.40, 0.32), arrowprops=arrow)
ax.text(0.42, 0.20, r"$\chi_{\mu\nu}$", color=CRED,
        fontsize=12, ha="left", va="top")

ax.set_xlim(-0.62, 1.62)
ax.set_ylim(-0.42, 1.22)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-045.pdf")
fig.savefig("../fig-redraw-045.png", dpi=200)
print("done")

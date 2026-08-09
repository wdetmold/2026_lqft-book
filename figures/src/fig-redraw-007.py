"""Redraw of fig-notes-007: region of the O(n) phase diagram controlled by
the hopping (kappa) expansion.

Gray region kappa/kappa_c < 0.95 is under control of the hopping expansion;
the critical line kappa/kappa_c = 1 (continuum limit) lies just above, and
one still needs to learn how to bridge the gap.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

C_RED = "#D55E00"
C_GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(4.6, 3.0))

# region controlled by the hopping expansion
ax.axhspan(0.0, 0.95, color="0.92", zorder=0)

# critical line kappa/kappa_c = 1 (continuum limit)
ax.plot([0, 1], [1, 1], color=C_RED, lw=2.6, zorder=3,
        solid_capstyle="butt", clip_on=False)

# arrows from the controlled region up towards the critical line
for x0 in (0.14, 0.32, 0.50, 0.68, 0.86):
    ax.annotate("", xy=(x0, 0.985), xytext=(x0, 0.83),
                arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=1.5,
                                mutation_scale=13), zorder=2)

# ---- direct labels ---------------------------------------------------------
ax.annotate("critical line (continuum limit)", xy=(0.16, 1.008),
            xytext=(0.52, 1.10), color=C_RED, ha="center", va="bottom",
            fontsize=10,
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=0.9,
                            connectionstyle="arc3,rad=0.25",
                            shrinkA=4, shrinkB=2))
ax.annotate("need to learn how to get here", xy=(0.77, 0.955),
            xytext=(0.60, 0.58), color=C_GREEN, ha="center", va="center",
            fontsize=10,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.75,
                      pad=1.5),
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=0.9,
                            connectionstyle="arc3,rad=-0.25",
                            shrinkA=6, shrinkB=2))

# ---- axes ------------------------------------------------------------------
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.22)
ax.set_xticks([0, 1])
ax.set_xticklabels(["0", r"$\infty$"])
ax.set_yticks([0, 0.95, 1.0])
ax.set_yticklabels(["0", "0.95", "1"])
ax.minorticks_off()
ax.tick_params(length=0)
# keep the 0.95 and 1 tick labels from colliding
ax.get_yticklabels()[1].set_verticalalignment("top")
ax.get_yticklabels()[2].set_verticalalignment("bottom")
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$\kappa/\kappa_c$")

fig.tight_layout(pad=0.4)
fig.savefig("../fig-redraw-007.pdf")
fig.savefig("../fig-redraw-007.png", dpi=200)
print("done 007")

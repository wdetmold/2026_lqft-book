"""Redraw of fig-notes-079: a Markov-chain time history of an observable A,
showing initial thermalisation, fluctuations about equilibrium, and
approximately independent samples (crosses) retained after each
autocorrelation time."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

VERM = "#D55E00"
BLUE = "#0072B2"
DARK = "0.25"

rng = np.random.default_rng(0)

# Time history: exponential thermalisation plus smoothed noise.
n = 1200
t = np.linspace(0.0, 1.0, n)
base = 0.32 + 0.52 * np.exp(-t / 0.115)
noise = rng.normal(0.0, 1.0, n)
kern = np.exp(-np.arange(40) / 8.0)
noise = np.convolve(noise, kern / kern.sum(), mode="same")
A = base + 0.030 * noise / noise.std()

t_th = 0.33                     # end of thermalisation
tau = 0.105                     # sample spacing (~ 2 tau_int)
t_samp = np.arange(t_th + 0.06, 1.0, tau)
A_samp = np.interp(t_samp, t, A)


def brace(ax, x0, x1, y, h, color, lw=1.1):
    """Curly brace spanning [x0, x1] at height y; tip displaced by h."""
    res = 601
    beta = 260.0 / (x1 - x0)
    x = np.linspace(x0, x1, res)
    xh = x[: res // 2 + 1]
    prof = (1.0 / (1.0 + np.exp(-beta * (xh - x0)))
            + 1.0 / (1.0 + np.exp(-beta * (xh - xh[-1]))))
    prof = np.concatenate((prof, prof[-2::-1]))
    y_br = y + h * (prof - 0.5)
    ax.plot(x, y_br, color=color, lw=lw, clip_on=False, zorder=4)


fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.axis("off")

# Axes drawn as arrows.
ax.annotate("", xy=(1.06, 0.0), xytext=(-0.02, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            mutation_scale=12))
ax.annotate("", xy=(0.0, 1.02), xytext=(0.0, -0.02),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=0.9,
                            mutation_scale=12))
ax.text(-0.035, 1.0, r"$A$", fontsize=12, ha="right", va="top")
ax.text(1.055, 0.035, "Markov time", fontsize=10, ha="right", va="bottom")

ax.plot(t, A, color=VERM, lw=1.1, zorder=3)

# Approximately independent samples.
ax.scatter(t_samp, A_samp, s=48, marker="x", color=BLUE, lw=1.5, zorder=5)

# Thermalisation brace (below the axis).
brace(ax, 0.01, t_th, -0.075, -0.05, DARK)
ax.text(0.5 * t_th, -0.175, "thermalisation", fontsize=10,
        ha="center", va="top", color=DARK)

# Braces marking successive autocorrelation intervals.
for k in range(len(t_samp) - 1):
    brace(ax, t_samp[k] + 0.008, t_samp[k + 1] - 0.008, -0.075, -0.045, DARK)
ax.text(0.5 * (t_samp[0] + t_samp[1]), -0.165, r"$\tau_{\mathrm{int},A}$",
        fontsize=10, ha="center", va="top", color=DARK)

# Annotation over the equilibrium samples.
brace(ax, t_samp[0] - 0.02, t_samp[-1] + 0.02, 0.52, 0.05, DARK)
ax.text(0.5 * (t_samp[0] + t_samp[-1]), 0.62,
        "approx. independent samples\n"
        r"distributed according to $P_{\mathrm{eq}}(s)$",
        fontsize=9.5, ha="center", va="bottom", color=DARK)

ax.set_xlim(-0.06, 1.08)
ax.set_ylim(-0.28, 1.05)

fig.savefig("../fig-redraw-079.pdf")
fig.savefig("../fig-redraw-079.png", dpi=200)
print("done 079")

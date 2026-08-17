"""The free Kaehler-Dirac spectrum on D_4, with Z^4 for comparison.

(a) all 72 branches of K = d - delta along a path through the D_4 Brillouin
    zone: 16 light branches with a single isotropic velocity, 56 gapped at
    the cutoff.
(b) the discretisation error of the light dispersion, D_4 against Z^4:
    both O(a^2), but D_4's is direction-independent.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from complex import build_D4, build_Z4
plt.style.use("lqftbook.mplstyle")

C4, CZ = build_D4(), build_Z4()
W4 = {0: 2.0, 1: 1/3, 2: 0.5, 3: 3.0, 4: 1.5}
WZ = {p: 1.0 for p in range(5)}

def br(C, w, k):
    D, _, _ = C.bloch_d(k)
    s = np.concatenate([np.full(C.n[p], np.sqrt(w[p])) for p in range(5)])
    Dt = (s[:, None] * D) / s[None, :]
    return np.sort(np.abs(np.linalg.eigvals(Dt - Dt.conj().T)))

# path Gamma -> X -> W -> Gamma  in the D_4 BZ (points of the bcc-like dual)
G = np.zeros(4)
N = np.pi*np.array([1, 0, 0, 0])          # BZ face centre (half of 2*pi*e_1)
P = np.pi/2*np.array([1, 1, 1, 1])        # BZ face centre (half of pi*(1,1,1,1))
pts = [G, N, P, G]
names = [r"$\Gamma$", r"$N$" "\n" r"$(\pi,0,0,0)$",
         r"$P$" "\n" r"$\frac{\pi}{2}(1,1,1,1)$", r"$\Gamma$"]
NS = 46
path, ticks = [], [0]
for a, b in zip(pts[:-1], pts[1:]):
    for i in range(NS):
        path.append(a + (b - a)*i/NS)
    ticks.append(len(path))
path.append(pts[-1]); path = np.array(path)
x = np.zeros(len(path))
for i in range(1, len(path)): x[i] = x[i-1] + np.linalg.norm(path[i]-path[i-1])

S = np.array([br(C4, W4, k) for k in path])
SZ = np.array([br(CZ, WZ, k) for k in path])

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3))

ax = axes[0]
for j in range(16, 72):
    ax.plot(x, S[:, j], color="#BFC9D2", lw=0.7, zorder=1)
for j in range(16):
    ax.plot(x, S[:, j], color="#0072B2", lw=1.1, zorder=3)
ax.axhline(2*np.sqrt(2), color="#D55E00", lw=0.9, ls="--", zorder=2)
ax.text(x[-1]*0.985, 2*np.sqrt(2)+0.16, r"$2\sqrt{2}$", color="#D55E00",
        fontsize=8.5, ha="right")
for t in ticks[1:-1]: ax.axvline(x[t], color="#999999", lw=0.6)
ax.set_xticks([x[t] for t in ticks]); ax.set_xticklabels(names)
ax.set_xlim(0, x[-1]); ax.set_ylim(0, 9)
ax.set_ylabel(r"$|\lambda(k)|$")
ax.set_title(r"(a) $D_4$: $72$ branches of $d-\delta$", fontsize=9.6)
ax.text(x[ticks[1]]*0.34, 1.05, r"$16$ light", color="#0072B2", fontsize=9)
ax.text(x[ticks[1]]*0.30, 6.6, r"$56$ gapped", color="#8A96A3", fontsize=9)

ax = axes[1]
ks = np.linspace(0.05, 0.9, 26)
lab = {(1,0,0,0): r"$(1,0,0,0)$", (1,1,0,0): r"$(1,1,0,0)$",
       (1,1,1,1): r"$(1,1,1,1)$"}
for d, ls in zip(lab, ("-", "--", ":")):
    dn = np.array(d, float); dn /= np.linalg.norm(dn)
    yz = [br(CZ, WZ, kk*dn)[:16].mean()/kk - 1 for kk in ks]
    ax.plot(ks, np.abs(yz), ls, color="#D55E00", lw=1.2)
    y4 = [br(C4, W4, kk*dn)[:16].mean()/kk - 1 for kk in ks]
    ax.plot(ks, np.abs(y4), ls, color="#0072B2", lw=1.2)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$|k|$ (lattice units)")
ax.set_ylabel(r"$|\lambda/|k| - 1|$")
ax.set_title(r"(b) discretisation error of the light modes", fontsize=9.6)
ax.text(0.30, 2.6e-2, r"$\mathbb{Z}^4$", color="#D55E00", fontsize=10)
ax.text(0.62, 3.0e-3, r"$D_4$", color="#0072B2", fontsize=10)
ax.text(0.98, 6e-5, "three directions each;\n" r"the $D_4$ curves coincide",
        fontsize=7.8, color="#444444", va="bottom", ha="right")
fig.tight_layout(pad=0.5)
fig.savefig("fig-d4-kahler-dirac.pdf")
fig.savefig("fig-d4-kahler-dirac.png", dpi=200)
print("wrote fig-d4-kahler-dirac")

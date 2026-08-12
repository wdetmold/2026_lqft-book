"""
free_anisotropy.py -- exact (no Monte Carlo) demonstration that the leading
rotational-symmetry-breaking artifact of the free scalar propagator is

        O(a^2)  on the hypercubic lattice Z^4,
        O(a^4)  on the D_4 checkerboard lattice.

--------------------------------------------------------------------------
WHAT IS COMPUTED
--------------------------------------------------------------------------
The free lattice propagator on a periodic L^4 box,

        G(x) = (1/L^4) sum_p  e^{i p.x} / ( Khat(p) + m^2 ),
        p = 2 pi k / L,  k in Z_L^4,

        Khat(p) = (1/c) sum_{e in shell} 2 ( 1 - cos(p.e) ) ,

with the shell being the 24 vectors (+-1,+-1,0,0) for D_4 and the 8 vectors
(+-1,0,0,0) for Z^4.  The constant c is the small-p normalisation
(c = 12 for D_4, c = 1 for Z^4, since sum_e (p.e)^2 = 12 p^2 and 2 p^2
respectively), chosen so that Khat(p) = p^2 + O(p^4) on BOTH lattices.  With
that convention the tree-level correlation length in lattice units is
xi = 1/m for both, and the two lattices are compared at equal physical mass.
The overall normalisation is irrelevant for the anisotropy measure below,
which is a ratio.

Momentum-space kernels used (both derived by summing the shell in closed
form -- see the check at the bottom of the file):

        Khat_hc(p) = 8 - 2 sum_mu cos p_mu
        Khat_d4(p) = (8/12) * [ 6 - sum_{mu<nu} cos p_mu cos p_nu ] * ... :
                     sum over the 24 vectors gives
                     8 sum_{mu<nu} ( 1 - cos p_mu cos p_nu ),
                     which we then divide by c = 12.

Small-p expansion, using sum_e (p.e)^2 = 12 p^2 and sum_e (p.e)^4 = 12 (p^2)^2:

        Khat_hc = p^2 - (1/12) sum_mu p_mu^4 + ...      <- ANISOTROPIC at O(p^4)
        Khat_d4 = p^2 - (1/12) (p^2)^2 + O(p^6)         <- isotropic at O(p^4);
                                                           the first anisotropy
                                                           is the F_4 invariant
                                                           hiding in sum_e (p.e)^6

Relative to the leading p^2 the artifact is therefore O(p^2) ~ O(a^2) for
hypercubic and O(p^4) ~ O(a^4) for D_4.

--------------------------------------------------------------------------
WHAT IS COMPARED, AND WHY *NOT* (2,0,0,0) vs (1,1,1,1)
--------------------------------------------------------------------------
The anisotropy estimator is the pair asymmetry

        A(x_a, x_b) = 2 ( G(x_a) - G(x_b) ) / ( G(x_a) + G(x_b) ),
        with |x_a| = |x_b| exactly,

which vanishes identically in the rotationally invariant continuum theory.

The obvious candidate pairs -- "axis vs. body diagonal" at equal length,

        (2,0,0,0) vs (1,1,1,1)   [|x|^2 = 4]
        (4,0,0,0) vs (2,2,2,2)   [|x|^2 = 16]

-- are inequivalent on Z^4 but are related on D_4 by the triality reflection
H = (1/2)[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]] in W(F_4), the point
group of D_4 (order 1152).  On D_4 those two points sit in a SINGLE point-group
orbit, so G is exactly equal on them for a trivial symmetry reason and the
measured asymmetry is zero to machine precision -- it tells us nothing about
the order of the artifact.  Part 1 of this script demonstrates that explicitly.

The smallest D_4 shell carrying two distinct W(F_4) orbits is |x|^2 = 18.
We therefore use the scalable, genuinely inequivalent family

        x_a(lam) = lam * (3,3,0,0)        (orbit of size  24)
        x_b(lam) = lam * (4,1,1,0)        (orbit of size 288)
        |x| = lam * sqrt(18)  for both,  lam = 1,2,3,...

Both points have even coordinate sum for every lam, so they exist on D_4 as
well as on Z^4, which makes the comparison between the two lattices fair, and
they are inequivalent under the hyperoctahedral group B_4 too (the multisets
of |coordinates| differ), so the hypercubic asymmetry is nonzero as well.

--------------------------------------------------------------------------
HOW THE POWER IS EXTRACTED
--------------------------------------------------------------------------
Naively varying m at FIXED lattice separation x does not measure the order of
the artifact: for xi >> |x| the asymmetry saturates at the (mass independent)
short-distance value of the massless lattice propagator.  The continuum limit
is a -> 0 at FIXED physical separation R = a|x| and FIXED physical mass
M = 1/(a xi), i.e. |x| and xi must be sent to infinity together with

        rho = |x| / xi   held fixed.

We therefore scan lam = 1, 2, 3, ... and set xi = lam sqrt(18) / rho.  Then
1/xi plays the role of the lattice spacing a in units of the correlation
length, and

        |A| = C (1/xi)^n ,   n = 2 (hypercubic),  n = 4 (D_4).

Finite volume is the main systematic: the periodic sum equals the
infinite-volume propagator plus its images, and the leading image relative to
the signal is O(exp(-(L - 2|x|)/xi)), which is direction dependent and so
feeds straight into A.  Since the D_4 signal is only ~xi^-4, L must be
comfortably larger than 2|x| + n xi ln(...).  At the default L = 256 with
rho = 2.5 the estimated image contamination of the largest-xi point is ~2e-9
of G, i.e. ~1e-4 of the D_4 signal; the script prints an explicit
smaller-box cross-check so the reader can see the systematic appear.

--------------------------------------------------------------------------
ALGORITHM
--------------------------------------------------------------------------
G is needed at only a handful of points, but the momentum sum has L^4 terms
(4.3e9 at L = 256), which does not fit in memory as a single array.  Both
kernels are even in every p_mu separately, so the momentum sum reduces to a
type-I discrete cosine transform over the reduced range k_mu in [0, L/2].  We
loop over the outermost reduced momentum k_1 and do a 3d DCT-I of the
(L/2+1)^3 slice, giving L/2+1 slices of ~17 MB each.  Exact agreement with a
direct complex FFT is verified in `_check_kernels()`.

Usage
-----
    python3 free_anisotropy.py                 # defaults: L=256, rho=2.5
    python3 free_anisotropy.py --L 128 --lam-max 5   # ~15 s, same exponents
    python3 free_anisotropy.py --no-plot

Runtime: ~3 minutes at the default L = 256 on two cores; L = 128 takes ~15 s
and already gives the exponents to a few per cent.
"""

from __future__ import annotations

import argparse
import os
import time

import numpy as np
from scipy import fft

from d4lattice import d4_neighbours, hypercubic_neighbours, same_d4_orbit

STYLE_PATH = "/home/user/lqft-book/figures/src/lqftbook.mplstyle"

# Small-p normalisation constants: sum_{e in shell} (p.e)^2 = C_LEAD * p^2.
C_LEAD = {"d4": 12.0, "hc": 2.0}


# ==========================================================================
# Momentum-space kernel
# ==========================================================================
def khat_slice(c1: float, c2, c3, c4, lattice: str) -> np.ndarray:
    """Normalised kernel Khat(p) = p^2 + O(p^4), for cos p_1 = c1 fixed.

    c2, c3, c4 are broadcastable arrays of cos p_2, cos p_3, cos p_4.

    Summing 2(1 - cos(p.e)) over the FULL shell (8 resp. 24 vectors, i.e. e
    and -e both counted) and dividing by c = sum_e (p.e)^2 / p^2 gives

      hypercubic:  [ 4 sum_mu (1 - cos p_mu) ] / 2   = 8 - 2 sum_mu cos p_mu
      D_4       :  [ 8 sum_{mu<nu} (1 - c_mu c_nu) ] / 12

    The D_4 form follows from pairing the four sign choices of (+-1,+-1,0,0):
        2(1-cos(p_mu+p_nu)) + 2(1-cos(p_mu-p_nu)) = 4 - 4 cos p_mu cos p_nu,
    counted twice (the two overall signs), summed over the 6 pairs {mu,nu}.
    """
    if lattice == "d4":
        pair = (c1 * c2 + c1 * c3 + c1 * c4 + c2 * c3 + c2 * c4 + c3 * c4)
        return (8.0 / C_LEAD["d4"]) * (6.0 - pair)
    if lattice == "hc":
        return (4.0 / C_LEAD["hc"]) * (4.0 - (c1 + c2 + c3 + c4))
    raise ValueError(lattice)


def propagator_at(L: int, m2: float, lattice: str, pts) -> np.ndarray:
    """G(x) at the listed points by exact summation over the L^4 momenta.

    Uses the reflection symmetry k_mu -> -k_mu of the kernel to replace the
    complex FFT by a type-I DCT over k_mu in [0, L/2].  Requires every
    coordinate of every point to satisfy 0 <= x_mu <= L/2 (call sites reduce
    x modulo the box symmetries themselves).

    Parameters
    ----------
    L    : even box size
    m2   : mass squared in lattice units (xi = 1/sqrt(m2) at tree level)
    pts  : sequence of integer 4-tuples
    """
    assert L % 2 == 0
    pts = [tuple(int(v) for v in p) for p in pts]
    for p in pts:
        assert all(0 <= v <= L // 2 for v in p), f"point {p} outside [0, L/2]^4"

    n = L // 2 + 1
    c = np.cos(2.0 * np.pi * np.arange(n) / L)
    c2 = c[:, None, None]
    c3 = c[None, :, None]
    c4 = c[None, None, :]

    # DCT-I weights for the reduced k_1 sum: endpoints once, interior twice.
    w = np.full(n, 2.0)
    w[0] = 1.0
    w[-1] = 1.0

    x1 = np.array([p[0] for p in pts])
    acc = np.zeros(len(pts))
    for k1 in range(n):
        d = 1.0 / (khat_slice(c[k1], c2, c3, c4, lattice) + m2)
        # dctn type 1 over the three inner axes == sum_k d cos(2 pi k x / L)
        f = fft.dctn(d, type=1, axes=(0, 1, 2), workers=-1)
        phase = np.cos(2.0 * np.pi * k1 * x1 / L)
        for i, (_, a, b, cc) in enumerate(pts):
            acc[i] += w[k1] * phase[i] * f[a, b, cc]
    return acc / L ** 4


def asymmetry(ga: float, gb: float) -> float:
    """Dimensionless pair anisotropy A = 2 (Ga - Gb) / (Ga + Gb)."""
    return 2.0 * (ga - gb) / (ga + gb)


# ==========================================================================
# Sanity checks on the kernel and the transform
# ==========================================================================
def _check_kernels() -> None:
    """Verify (i) the closed-form kernels against a brute-force shell sum and
    (ii) the DCT-I propagator against a direct complex FFT, on a small box."""
    rng = np.random.default_rng(1)
    p = rng.normal(size=(6, 4))
    for lattice, shell in (("d4", d4_neighbours()), ("hc", hypercubic_neighbours())):
        brute = (2.0 * (1.0 - np.cos(p @ shell.T))).sum(1) / C_LEAD[lattice]
        cc = np.cos(p)
        closed = np.array([khat_slice(cc[i, 0], cc[i, 1], cc[i, 2], cc[i, 3], lattice)
                           for i in range(len(p))])
        assert np.allclose(brute, closed), lattice
        # small-p normalisation: Khat -> p^2
        q = 1e-4 * rng.normal(size=4)
        cq = np.cos(q)
        k = khat_slice(cq[0], cq[1], cq[2], cq[3], lattice)
        assert abs(k / (q @ q) - 1.0) < 1e-6, (lattice, k / (q @ q))
    print("  closed-form kernels match the brute-force shell sums, and both "
          "are normalised to Khat -> p^2.")

    # DCT-I vs. direct complex FFT on a small box
    L, m2 = 24, 0.25
    pts = [(3, 3, 0, 0), (4, 1, 1, 0)]
    for lattice in ("d4", "hc"):
        g_dct = propagator_at(L, m2, lattice, pts)
        k = np.arange(L)
        c = np.cos(2 * np.pi * k / L)
        acc = np.zeros(len(pts))
        for k1 in range(L):
            d = 1.0 / (khat_slice(c[k1], c[:, None, None], c[None, :, None],
                                  c[None, None, :], lattice) + m2)
            f = fft.rfftn(d, workers=-1).real
            for i, (a, b, cc_, dd) in enumerate(pts):
                acc[i] += np.cos(2 * np.pi * k1 * a / L) * f[b, cc_, dd]
        g_fft = acc / L ** 4
        rel = np.max(np.abs(g_dct / g_fft - 1.0))
        assert rel < 1e-10, (lattice, rel)
    print("  DCT-I momentum sum agrees with the direct complex FFT to "
          f"{rel:.1e} relative.")


# ==========================================================================
# Part 1: the triality trap
# ==========================================================================
def triality_demo(L: int, xi: float) -> None:
    """Show that the 'obvious' axis/diagonal pairs are exactly degenerate on
    D_4 (single W(F_4) orbit) but not on Z^4."""
    print()
    print("-" * 74)
    print("PART 1  Why (2,0,0,0) vs (1,1,1,1) is the WRONG pair on D_4")
    print("-" * 74)
    print(f"  box L = {L}, xi = {xi:g}  (m^2 = {1.0 / xi ** 2:g})")
    print()
    hdr = (f"{'pair':>28} {'|x|^2':>6} {'same W(F4) orbit':>17} "
           f"{'A(hypercubic)':>15} {'A(D_4)':>13}")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    pairs = [((2, 0, 0, 0), (1, 1, 1, 1)),
             ((4, 0, 0, 0), (2, 2, 2, 2)),
             ((3, 3, 0, 0), (4, 1, 1, 0)),
             ((6, 0, 0, 0), (4, 4, 2, 0))]
    m2 = 1.0 / xi ** 2
    for xa, xb in pairs:
        row = {}
        for lattice in ("hc", "d4"):
            g = propagator_at(L, m2, lattice, [xa, xb])
            row[lattice] = asymmetry(g[0], g[1])
        n2 = sum(v * v for v in xa)
        print(f"{str(xa) + ' vs ' + str(xb):>28} {n2:6d} "
              f"{str(same_d4_orbit(xa, xb)):>17} "
              f"{row['hc']:+15.6e} {row['d4']:+13.6e}")
    print()
    print("  The first two pairs are one W(F_4) orbit: A(D_4) is zero to")
    print("  round-off (the residue is the O(exp(-L/2 xi)) triality breaking")
    print("  of the torus, not a lattice artifact).  The |x|^2 = 18 and 36")
    print("  pairs are genuinely inequivalent and are what we scale below.")


# ==========================================================================
# Part 2: the continuum-limit scan
# ==========================================================================
BASE_A = np.array([3, 3, 0, 0])
BASE_B = np.array([4, 1, 1, 0])
BASE_NORM = float(np.sqrt((BASE_A ** 2).sum()))  # sqrt(18)


def scaling_scan(L: int, rho: float, lams) -> dict:
    """For each lam: |x| = lam sqrt(18), xi = |x|/rho, measure A on both lattices."""
    out = {"lam": [], "r": [], "xi": [], "hc": [], "d4": [],
           "g_hc": [], "g_d4": []}
    for lam in lams:
        xa = tuple(lam * BASE_A)
        xb = tuple(lam * BASE_B)
        r = lam * BASE_NORM
        xi = r / rho
        m2 = 1.0 / xi ** 2
        assert max(max(xa), max(xb)) <= L // 2, (
            f"lam={lam} needs L >= {2 * max(max(xa), max(xb))}")
        rec = {}
        for lattice in ("hc", "d4"):
            g = propagator_at(L, m2, lattice, [xa, xb])
            rec[lattice] = g
            out[lattice].append(asymmetry(g[0], g[1]))
            out["g_" + lattice].append(tuple(g))
        out["lam"].append(lam)
        out["r"].append(r)
        out["xi"].append(xi)
    for k in ("r", "xi", "hc", "d4"):
        out[k] = np.array(out[k])
    return out


def fit_power(xi: np.ndarray, a: np.ndarray, drop: int = 0):
    """Least-squares fit log|A| = log C + n log(1/xi); returns (n, logC)."""
    x = np.log(1.0 / xi[drop:])
    y = np.log(np.abs(a[drop:]))
    n, logc = np.polyfit(x, y, 1)
    return float(n), float(logc)


def local_slopes(xi: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Successive two-point slopes d log|A| / d log(1/xi)."""
    x = np.log(1.0 / xi)
    y = np.log(np.abs(a))
    return np.diff(y) / np.diff(x)


# ==========================================================================
# Plot
# ==========================================================================
def make_plot(res: dict, fits: dict, outstem: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    try:
        plt.style.use(STYLE_PATH)
    except OSError:
        print(f"  (house style {STYLE_PATH} not found; using defaults)")

    colours = {"hc": "#D55E00", "d4": "#0072B2"}
    labels = {"hc": "hypercubic $Z^4$", "d4": "$D_4$"}

    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    inv = 1.0 / res["xi"]
    xline = np.array([inv.min() * 0.82, inv.max() * 1.12])

    for lat in ("hc", "d4"):
        n, logc = fits[lat]
        ax.plot(xline, np.exp(logc) * xline ** n, color=colours[lat],
                lw=0.9, ls="--", zorder=1)
        ax.plot(inv, np.abs(res[lat]), "o", color=colours[lat], ms=4.2,
                zorder=3, mfc="white", mew=1.2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$1/\xi$   (lattice spacing in units of $\xi$)")
    ax.set_ylabel(r"$|A| = |2(G_a-G_b)/(G_a+G_b)|$")

    # head-room so the direct labels sit inside the axes
    amin = min(np.abs(res["d4"]).min(), np.abs(res["hc"]).min())
    amax = max(np.abs(res["d4"]).max(), np.abs(res["hc"]).max())
    ax.set_xlim(xline[0], xline[1])
    ax.set_ylim(amin / 10.0, amax * 10.0)

    # direct labels, no legend box: anchored on a mid-curve point, offset
    # perpendicular to the line
    def direct_label(lat, ipt, dy, va):
        n = fits[lat][0]
        ax.text(inv[ipt], np.abs(res[lat])[ipt] * dy,
                f"{labels[lat]}\n$|A|\\propto a^{{{n:.2f}}}$",
                color=colours[lat], ha="center", va=va, fontsize=8.5,
                linespacing=1.4)

    direct_label("hc", 2, 5.0, "bottom")
    direct_label("d4", 3, 0.20, "top")

    # a single "10^-1" decade tick is not informative on this narrow range
    from matplotlib.ticker import (FixedLocator, FuncFormatter, LogLocator,
                                   NullFormatter)
    ticks = [t for t in (0.1, 0.15, 0.2, 0.3, 0.5) if xline[0] <= t <= xline[1]]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())

    fig.savefig(outstem + ".pdf")
    fig.savefig(outstem + ".png")
    plt.close(fig)
    print(f"\n  wrote {outstem}.pdf and {outstem}.png")


# ==========================================================================
# Main
# ==========================================================================
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--L", type=int, default=256,
                    help="periodic box side (even). default 256")
    ap.add_argument("--rho", type=float, default=2.5,
                    help="fixed physical ratio |x|/xi. default 2.5")
    ap.add_argument("--lam-max", type=int, default=6,
                    help="largest scale factor lam. default 6")
    ap.add_argument("--drop", type=int, default=2,
                    help="coarsest points dropped from the asymptotic fit. "
                         "default 2")
    ap.add_argument("--no-plot", action="store_true")
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()

    L = args.L
    assert L % 2 == 0, "L must be even"

    t0 = time.time()
    print("=" * 74)
    print("free_anisotropy.py -- rotational-symmetry artifacts of the free "
          "lattice scalar")
    print("=" * 74)
    print("\nSanity checks:")
    _check_kernels()

    triality_demo(L=min(L, 64), xi=2.0)

    lams = list(range(1, args.lam_max + 1))
    need = 2 * args.lam_max * int(BASE_A.max())
    assert L >= need, f"L={L} too small for lam_max={args.lam_max}; need L >= {need}"

    print()
    print("-" * 74)
    print("PART 2  Continuum-limit scan at fixed rho = |x|/xi")
    print("-" * 74)
    print(f"  x_a = lam*(3,3,0,0),  x_b = lam*(4,1,1,0),  |x| = lam*sqrt(18)")
    print(f"  rho = |x|/xi = {args.rho:g}   box L = {L}")
    print()

    res = scaling_scan(L, args.rho, lams)

    hdr = (f"{'lam':>4} {'|x|':>7} {'xi':>7} {'1/xi':>8} | "
           f"{'G_a (hc)':>12} {'G_b (hc)':>12} {'A_hc':>12} | "
           f"{'G_a (D4)':>12} {'G_b (D4)':>12} {'A_D4':>12}")
    print(hdr)
    print("-" * len(hdr))
    for i, lam in enumerate(res["lam"]):
        gh = res["g_hc"][i]
        gd = res["g_d4"][i]
        print(f"{lam:4d} {res['r'][i]:7.3f} {res['xi'][i]:7.3f} "
              f"{1 / res['xi'][i]:8.5f} | "
              f"{gh[0]:12.5e} {gh[1]:12.5e} {res['hc'][i]:+12.5e} | "
              f"{gd[0]:12.5e} {gd[1]:12.5e} {res['d4'][i]:+12.5e}")

    print("\n  local two-point slopes  d log|A| / d log(1/xi):")
    for lat, tag in (("hc", "hypercubic"), ("d4", "D_4       ")):
        sl = local_slopes(res["xi"], res[lat])
        print(f"    {tag} : " + "  ".join(f"{s:6.3f}" for s in sl))

    fits = {}
    print("\n  power-law fits  |A| = C (1/xi)^n :")
    print(f"    {'lattice':<12} {'n (all pts)':>12} "
          f"{'n (drop %d coarsest)' % args.drop:>22} {'expected':>10}")
    for lat, tag, exp in (("hc", "hypercubic", 2), ("d4", "D_4", 4)):
        n_all, _ = fit_power(res["xi"], res[lat], drop=0)
        n_as, logc = fit_power(res["xi"], res[lat], drop=args.drop)
        fits[lat] = (n_as, logc)
        print(f"    {tag:<12} {n_all:12.3f} {n_as:22.3f} {exp:10d}")

    # ---- finite-volume cross-check --------------------------------------
    # The periodic momentum sum returns  sum_n G_inf(x + L n), so the leading
    # systematic on A is the direction dependence of the nearest image,
    # relative size ~ exp(-(L - 2|x|)/xi).  We verify by repeating the
    # largest-xi (hence most vulnerable) point in a smaller box.
    lam = lams[-1]
    xa, xb = tuple(lam * BASE_A), tuple(lam * BASE_B)
    xi = lam * BASE_NORM / args.rho
    r = lam * BASE_NORM
    Lc = max(2 * int(BASE_A.max()) * lam, 2 * ((3 * L // 4) // 2))
    print(f"\n  finite-volume cross-check on the largest-xi point "
          f"(lam = {lam}, xi = {xi:.3f}), L = {Lc} vs L = {L}:")
    print(f"    naive image estimate exp(-(L-2|x|)/xi): "
          f"L={Lc}: {np.exp(-(Lc - 2 * r) / xi):.1e},  "
          f"L={L}: {np.exp(-(L - 2 * r) / xi):.1e}")
    for lat in ("hc", "d4"):
        g = propagator_at(Lc, 1.0 / xi ** 2, lat, [xa, xb])
        a_small = asymmetry(g[0], g[1])
        a_big = res[lat][-1]
        drift = abs(a_big / a_small - 1.0)
        print(f"    {lat:<4} A(L={Lc}) = {a_small:+.6e}   "
              f"A(L={L}) = {a_big:+.6e}   relative drift {drift:.2e}")

    if not args.no_plot:
        make_plot(res, fits, os.path.join(args.outdir, "anisotropy"))

    print(f"\n  total wall time {time.time() - t0:.1f} s")
    print("=" * 74)


if __name__ == "__main__":
    main()

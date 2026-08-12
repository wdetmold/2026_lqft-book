"""
wolff_ising.py -- Wolff single-cluster Monte Carlo for the Ising-limit scalar
(phi -> +-1) on the D_4 checkerboard lattice and on the hypercubic lattice Z^4,
using the neighbour tables built by d4lattice.py.

--------------------------------------------------------------------------
MODEL AND ALGORITHM
--------------------------------------------------------------------------
The Ising limit of the single-component lattice scalar,

        S = -beta sum_{<ij>} s_i s_j ,   s_i = +-1,

where <ij> runs over the nearest-neighbour bonds of the chosen lattice: 4 L^4
bonds (coordination 8) on Z^4 and 12 L^4 bonds (coordination 24) on D_4,
whose sites are the even-coordinate-sum points of Z_L^4.

Wolff single-cluster update: pick a random seed, flip it, and grow a cluster
by adding each aligned neighbour across a bond with probability

        p_add = 1 - exp(-2 beta) ,

flipping sites as they are added.  The algorithm is implemented shell by
shell with numpy so that the whole growth frontier is processed in one
vectorised pass.  For the single-cluster algorithm the mean cluster size is
the improved estimator of the magnetic susceptibility, <|C|> = chi, which we
also use for the crude beta_c scan.

--------------------------------------------------------------------------
WHERE IS beta_c?
--------------------------------------------------------------------------
Mean field gives beta_c ~ 1/q, i.e.

        Z^4  (q =  8) :  beta_c^MF = 0.125     ; literature  beta_c = 0.149694
        D_4  (q = 24) :  beta_c^MF = 1/24 = 0.041667

(4d Ising sits at its upper critical dimension, so the exponents are
mean-field up to logarithms.)  Mean field underestimates beta_c by ~20 % on
Z^4.  For D_4 no standard value was to hand, so it was measured here by
Binder-cumulant crossings U_L = 1 - <m^4>/(3<m^2>^2) between L = 8 and
L = 12 (9000 clusters per point):

        beta   U(L=8)      U(L=12)
        0.0450 0.277(25)   0.195(35)
        0.0455 0.389(19)   0.326(35)
        0.0460 0.466(12)   0.545(11)     -> crossing near beta = 0.0457

so we adopt  beta_c(D_4) = 0.0457, uncertain by roughly +-0.0010.  This is a
CRUDE number from two small volumes; it is good enough to sit near
criticality but should not be quoted as a determination.  `--scan` reruns a
(cheaper, susceptibility-based) version of the scan.

--------------------------------------------------------------------------
MEASUREMENT
--------------------------------------------------------------------------
The two-point function is measured for all separations at once by embedding
the spin configuration in the full L^4 grid (zeros on the odd-sum sites for
D_4) and using the FFT autocorrelation

        C(x) = sum_y s(y) s(y+x) = irfftn( |rfftn(s)|^2 ),
        G(x) = C(x) / N_sites .

For x on D_4 both y and y+x are D_4 sites, so the normalisation N_sites =
L^4/2 is exact.  This is a translation average over the whole lattice, which
is what makes a short run usable.

The anisotropy estimator is the same as in free_anisotropy.py,

        A = 2 ( G(x_a) - G(x_b) ) / ( G(x_a) + G(x_b) ),   |x_a| = |x_b| ,

evaluated on four pairs (all with max coordinate <= L/2 = 8 at the default
L = 16, so none of them wraps):

  TRIALITY pairs, a single W(F_4) orbit on D_4 but two distinct B_4 orbits
  on Z^4 -- so G is EXACTLY equal on them on D_4 and the estimator must come
  out zero within errors, while on Z^4 it is large:

        (2,0,0,0) vs (1,1,1,1)      |x|^2 =  4
        (4,0,0,0) vs (2,2,2,2)      |x|^2 = 16

  GENUINELY INEQUIVALENT pairs, two distinct W(F_4) orbits, where D_4 also
  has a nonzero artifact but a parametrically smaller one:

        (3,3,0,0) vs (4,1,1,0)      |x|^2 = 18   (smallest such D_4 shell)
        (6,0,0,0) vs (4,4,2,0)      |x|^2 = 36

At beta_c the correlator behaves as G(x) ~ |x|^{-(d-2+eta)} with eta = 0, so
the only scale is |x| itself and the anisotropy is expected to fall as
(a/|x|)^2 on Z^4 and (a/|x|)^4 on D_4.  At L = 16 only |x| = sqrt(18) and 6
are available, |x| is only a few lattice spacings, and G is contaminated by
the large finite-volume constant that a critical correlator develops on a
torus (sum_x G(x) = chi, so a critical run has G(x) ~ chi/N almost
independent of x at these distances).  This run is therefore a QUALITATIVE
check -- correct signs, decreasing G, the exact triality zero on D_4, and
|A_D4| << |A_hc| on the |x|^2 = 36 pair -- and NOT a continuum-limit
extraction.  Extracting the powers of a is the job of free_anisotropy.py.

The torus itself breaks triality (H maps (L,0,0,0) to (L/2,L/2,L/2,L/2),
which is not in L Z^4), by an amount O(exp(-L/2 xi)).  At criticality on
L = 16 that is not parametrically small, so a small nonzero A on the D_4
triality pairs would be a boundary-condition effect, not a lattice artifact.

Two versions of A are printed.  The first uses G(x) as measured.  The second
uses the connected correlator G_c(x) = G(x) - m^2, with m the magnetisation of
that configuration: on a torus sum_x G(x) = M^2/N over N separations, so a
critical G(x) sits on top of an x-independent pedestal <m^2> that dilutes the
ratio.  Subtracting it sharpens the short-distance pairs but amplifies the
noise at large |x|, where G_c is itself small.

Errors are jackknife over blocks of measurements; the jackknife is applied to
the ratio A, not to G_a and G_b separately, so the (strong) correlation
between the two is handled correctly.

Usage
-----
    python3 wolff_ising.py                     # defaults, ~2 min
    python3 wolff_ising.py --scan              # add the beta_c scan first
    python3 wolff_ising.py --L 16 --clusters 8000 --lattice d4

Runtime with the defaults (L = 16, 2000 thermalisation + 20000 measured
clusters per lattice, at beta_c): about 2 minutes total on two cores.
"""

from __future__ import annotations

import argparse
import time

import numpy as np

from d4lattice import make_lattice

# --------------------------------------------------------------------------
# Reference couplings.  Z^4: literature value.  D_4: from the --scan below.
# --------------------------------------------------------------------------
BETA_C = {"hc": 0.1496947,   # literature value for the 4d Ising model
          "d4": 0.0457}      # this work, crude Binder crossing (see docstring)
LATTICE_LABEL = {"hc": "hypercubic Z^4 (q=8)", "d4": "D_4 checkerboard (q=24)"}


# ==========================================================================
# Wolff single-cluster update
# ==========================================================================
def wolff_cluster(s: np.ndarray, nb: np.ndarray, p_add: float, rng) -> int:
    """Grow and flip one Wolff cluster in place; return its size.

    s   : (n_sites,) int8 array of +-1, modified in place
    nb  : (n_sites, q) neighbour table
    """
    seed = int(rng.integers(s.shape[0]))
    old = s[seed]
    s[seed] = -old
    frontier = np.array([seed], dtype=nb.dtype)
    size = 1
    while frontier.size:
        # every bond leaving the current shell, once per bond-direction
        cand = nb[frontier].ravel()
        cand = cand[s[cand] == old]            # still aligned & unflipped
        if cand.size == 0:
            break
        cand = cand[rng.random(cand.size) < p_add]
        if cand.size == 0:
            break
        # a site reachable over several bonds may appear more than once; it is
        # added if at least one bond activated, which np.unique implements
        cand = np.unique(cand)
        s[cand] = -old
        size += cand.size
        frontier = cand
    return size


# ==========================================================================
# Observables
# ==========================================================================
class Correlator:
    """FFT translation-averaged two-point function on the embedding L^4 grid."""

    def __init__(self, lat):
        self.L = lat.L
        self.n_sites = lat.n_sites
        x = lat.coords
        L = lat.L
        # flat row-major index of each lattice site inside the full L^4 grid
        self.flat = (((x[:, 0] * L + x[:, 1]) * L + x[:, 2]) * L + x[:, 3])
        self.grid = np.zeros(L ** 4, dtype=np.float64)

    def measure(self, s: np.ndarray) -> np.ndarray:
        L = self.L
        self.grid[:] = 0.0
        self.grid[self.flat] = s
        g = self.grid.reshape(L, L, L, L)
        f = np.fft.rfftn(g)
        c = np.fft.irfftn(f.real ** 2 + f.imag ** 2, s=(L, L, L, L),
                          axes=(0, 1, 2, 3))
        return c / self.n_sites          # G(x) for every x in the box


def energy_density(s: np.ndarray, nb: np.ndarray) -> float:
    """E/N = -(1/2N) sum_i sum_a s_i s_{nb(i,a)}  (each bond counted once)."""
    return -0.5 * float(np.mean(s[:, None] * s[nb], dtype=np.float64) * nb.shape[1])


# ==========================================================================
# Jackknife
# ==========================================================================
def jackknife(blocks: np.ndarray, func):
    """Jackknife mean and error of func(<blocks>) over the leading axis.

    blocks : (n_blocks, ...) array of per-block means of the raw quantities
    func   : maps a per-block-mean vector to the scalar estimator
    """
    blocks = np.asarray(blocks, dtype=float)
    n = blocks.shape[0]
    total = blocks.sum(axis=0)
    full = func(total / n)
    pseudo = np.array([func((total - blocks[i]) / (n - 1)) for i in range(n)])
    err = np.sqrt((n - 1) / n * np.sum((pseudo - pseudo.mean()) ** 2))
    return full, err


# ==========================================================================
# Point pairs
# ==========================================================================
#: (tag, x_a, x_b, note).  See the module docstring for why these four.
_PAIRS = [
    ("triality-4", (2, 0, 0, 0), (1, 1, 1, 1),
     "one W(F_4) orbit on D_4  -> A(D_4) = 0 by symmetry"),
    ("triality-16", (4, 0, 0, 0), (2, 2, 2, 2),
     "one W(F_4) orbit on D_4  -> A(D_4) = 0 by symmetry"),
    ("shell-18", (3, 3, 0, 0), (4, 1, 1, 0),
     "two W(F_4) orbits -> both lattices anisotropic"),
    ("shell-36", (6, 0, 0, 0), (4, 4, 2, 0),
     "two W(F_4) orbits -> both lattices anisotropic"),
]


def measurement_pairs(L: int):
    """(tag, x_a, x_b, |x|, note) for the pairs that fit in an L^4 box."""
    out = []
    for tag, xa, xb, note in _PAIRS:
        # require every coordinate strictly below L/2: at exactly L/2 a point
        # is its own periodic mirror image and the geometry is not comparable
        if max(max(xa), max(xb)) >= L // 2:
            continue
        out.append((tag, xa, xb, float(np.sqrt(sum(v * v for v in xa))), note))
    return out


# ==========================================================================
# Simulation driver
# ==========================================================================
def run(kind: str, L: int, beta: float, n_therm: int, n_meas: int,
        meas_every: int, n_blocks: int, seed: int, verbose: bool = True):
    rng = np.random.default_rng(seed)
    lat = make_lattice(kind, L)
    nb = lat.neighbours
    n = lat.n_sites
    p_add = 1.0 - np.exp(-2.0 * beta)

    # COLD start.  From a random (infinite-temperature) configuration the
    # Wolff branching ratio at beta_c is only ~(q-1) p_add / 2 ~ 1, so the
    # clusters stay microscopic and thermalisation takes enormous numbers of
    # updates.  Starting ordered puts the branching ratio safely above 1 and
    # the chain equilibrates within a few hundred clusters.
    s = np.ones(n, dtype=np.int8)
    corr = Correlator(lat)
    pairs = measurement_pairs(L)

    t0 = time.time()
    for _ in range(n_therm):
        wolff_cluster(s, nb, p_add, rng)
    t_therm = time.time() - t0

    # Raw per-measurement quantities, all block-averaged for the jackknife:
    #   [G(x_a), G(x_b)] for each pair, then |m|, the cluster size, and the
    #   L zero-spatial-momentum slice correlators Cbar(t) = sum_{x_1x_2x_3} G.
    npair = 2 * len(pairs)
    I_MABS, I_M2, I_CSZ = npair, npair + 1, npair + 2
    nq = npair + 3 + L
    raw = np.zeros((n_meas // meas_every, nq))
    csizes = []
    k = 0
    t0 = time.time()
    for it in range(n_meas):
        csizes.append(wolff_cluster(s, nb, p_add, rng))
        if (it + 1) % meas_every == 0:
            g = corr.measure(s)
            row = np.empty(nq)
            for i, (_, xa, xb, _, _) in enumerate(pairs):
                row[2 * i] = g[xa]
                row[2 * i + 1] = g[xb]
            mbar = s.mean()
            row[I_MABS] = abs(mbar)
            row[I_M2] = mbar * mbar     # the x-independent piece of G on a torus
            row[I_CSZ] = csizes[-1]
            row[I_CSZ + 1:] = g.sum(axis=(0, 1, 2))
            raw[k] = row
            k += 1
    t_meas = time.time() - t0
    raw = raw[:k]

    # block the measurement stream, then jackknife over blocks
    nb_use = min(n_blocks, k)
    cut = (k // nb_use) * nb_use
    blocks = raw[:cut].reshape(nb_use, -1, nq).mean(axis=1)

    # On a periodic torus a (near-)critical G(x) acquires an x-independent
    # piece:  sum_x G(x) = M^2/N over N values of x, so G(x) -> <m^2> at large
    # |x|.  That constant dilutes the anisotropy ratio, so we also quote the
    # connected estimator  G_c(x) = G(x) - m^2  (subtracted configuration by
    # configuration, so sum_x G_c = 0 exactly).
    results = []
    for i, (tag, xa, xb, r, note) in enumerate(pairs):
        ga, ea = jackknife(blocks, lambda b, i=i: b[2 * i])
        gb, eb = jackknife(blocks, lambda b, i=i: b[2 * i + 1])
        a, ea_ = jackknife(
            blocks, lambda b, i=i: 2.0 * (b[2 * i] - b[2 * i + 1])
                                   / (b[2 * i] + b[2 * i + 1]))
        ac, eac = jackknife(
            blocks, lambda b, i=i: 2.0 * (b[2 * i] - b[2 * i + 1])
                                   / (b[2 * i] + b[2 * i + 1] - 2.0 * b[I_M2]))
        results.append(dict(tag=tag, xa=xa, xb=xb, r=r, note=note,
                            Ga=ga, dGa=ea, Gb=gb, dGb=eb, A=a, dA=ea_,
                            Ac=ac, dAc=eac))

    mabs, dmabs = jackknife(blocks, lambda b: b[I_MABS])
    chi, dchi = jackknife(blocks, lambda b: b[I_CSZ])      # <|C|> = chi

    # Zero-spatial-momentum correlator and a mid-range effective mass; this is
    # only a sanity check that the run sits where we think it does.
    cbar = blocks[:, I_CSZ + 1:].mean(axis=0)
    t = max(2, L // 4)
    arg = (cbar[t - 1] + cbar[t + 1]) / (2.0 * cbar[t])
    xi_eff = 1.0 / np.arccosh(arg) if arg > 1.0 else np.inf

    info = dict(kind=kind, L=L, beta=beta, n_sites=n, q=lat.q,
                mean_cluster=float(np.mean(csizes)),
                cluster_frac=float(np.mean(csizes)) / n,
                mabs=mabs, dmabs=dmabs, chi=chi, dchi=dchi,
                cbar=cbar, xi_eff=float(xi_eff), xi_t=t,
                energy=energy_density(s, nb),
                t_therm=t_therm, t_meas=t_meas, n_blocks=nb_use,
                n_measurements=k)
    if verbose:
        _report(info, results)
    return info, results


def _report(info: dict, results: list) -> None:
    print()
    print("-" * 78)
    print(f"{LATTICE_LABEL[info['kind']]}   L = {info['L']}   "
          f"N = {info['n_sites']}   beta = {info['beta']:.6f}")
    print("-" * 78)
    print(f"  mean Wolff cluster size <|C|> = {info['mean_cluster']:.1f} "
          f"= {100 * info['cluster_frac']:.1f} % of the lattice "
          f"(= susceptibility chi)")
    print(f"  <|m|> = {info['mabs']:.5f} +- {info['dmabs']:.5f}    "
          f"E/N (last config) = {info['energy']:+.4f}")
    cb = info["cbar"]
    print(f"  zero-momentum slice correlator Cbar(t), t = 0..{min(6, len(cb) - 1)}: "
          + " ".join(f"{v:.3f}" for v in cb[:7]))
    print(f"  effective xi from cosh fit at t = {info['xi_t']}: "
          f"{info['xi_eff']:.2f}  (xi >~ L/2 means the run is critical and "
          f"G is dominated by the torus constant)")
    print(f"  {info['n_measurements']} measurements in {info['n_blocks']} "
          f"jackknife blocks;  therm {info['t_therm']:.1f} s, "
          f"measure {info['t_meas']:.1f} s")
    print()
    hdr = (f"    {'pair':>11} {'x_a':>12} {'x_b':>12} {'|x|':>6} "
           f"{'G(x_a)':>19} {'G(x_b)':>19} {'A':>18} {'A (m^2 subtr.)':>18}")
    print(hdr)
    print("    " + "-" * (len(hdr) - 4))
    for r in results:
        print(f"    {r['tag']:>11} {str(r['xa']):>12} {str(r['xb']):>12} "
              f"{r['r']:6.3f} "
              f"{r['Ga']:10.6f} +-{r['dGa']:7.6f} "
              f"{r['Gb']:10.6f} +-{r['dGb']:7.6f} "
              f"{r['A']:+9.4f} +-{r['dA']:6.4f} "
              f"{r['Ac']:+9.4f} +-{r['dAc']:6.4f}")
    for r in results:
        print(f"      {r['tag']:>8}: {r['note']}")


# ==========================================================================
# Crude beta_c scan
# ==========================================================================
def beta_scan(kind: str, L: int, betas, n_therm: int, n_clusters: int,
              seed: int) -> None:
    print()
    print("=" * 78)
    print(f"Crude beta_c scan -- {LATTICE_LABEL[kind]}, L = {L}")
    print("  <|C|> is the improved (single-cluster) estimator of chi.  With")
    print("  eta = 0 in four dimensions, finite-size scaling gives chi ~ L^2 at")
    print(f"  beta_c, i.e. <|C|>/N ~ L^-2 = {1.0 / L ** 2:.5f}; we quote the beta")
    print("  where the measured ratio crosses that value.")
    print("=" * 78)
    lat = make_lattice(kind, L)
    nb, n = lat.neighbours, lat.n_sites
    print(f"    {'beta':>9} {'<|C|>':>12} {'<|C|>/N':>10} {'<|m|>':>9}")
    out = []
    for beta in betas:
        rng = np.random.default_rng(seed)
        s = np.ones(n, dtype=np.int8)          # cold start, see run()
        p = 1.0 - np.exp(-2.0 * beta)
        for _ in range(n_therm):
            wolff_cluster(s, nb, p, rng)
        sizes, mags = [], []
        for _ in range(n_clusters):
            sizes.append(wolff_cluster(s, nb, p, rng))
            mags.append(abs(s.mean()))
        c = float(np.mean(sizes))
        out.append((beta, c / n))
        print(f"    {beta:9.4f} {c:12.1f} {c / n:10.4f} {np.mean(mags):9.4f}")
    # crude beta_c: where <|C|>/N crosses the finite-size-scaling value L^-2
    b = np.array([o[0] for o in out])
    f = np.array([o[1] for o in out])
    target = 1.0 / L ** 2
    idx = np.where((f[:-1] < target) & (f[1:] >= target))[0]
    if idx.size:
        i = int(idx[0])
        # linear interpolation in log(<|C|>/N)
        w = (np.log(target) - np.log(f[i])) / (np.log(f[i + 1]) - np.log(f[i]))
        bc = b[i] + w * (b[i + 1] - b[i])
        print(f"\n    crude beta_c ~ {bc:.4f}   "
              f"(mean field 1/q = {1.0 / lat.q:.4f}; "
              f"value adopted in BETA_C: {BETA_C[kind]:.4f})")
    else:
        print("\n    scan range does not bracket beta_c")


# ==========================================================================
# Main
# ==========================================================================
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--L", type=int, default=16, help="box side (even). default 16")
    ap.add_argument("--clusters", type=int, default=20000,
                    help="measured Wolff clusters per lattice. default 20000")
    ap.add_argument("--therm", type=int, default=2000,
                    help="thermalisation clusters. default 2000")
    ap.add_argument("--meas-every", type=int, default=10,
                    help="measure the correlator every this many clusters")
    ap.add_argument("--blocks", type=int, default=25,
                    help="jackknife blocks. default 25")
    ap.add_argument("--lattice", choices=["d4", "hc", "both"], default="both")
    ap.add_argument("--beta", type=float, default=None,
                    help="override beta (applied to every lattice run)")
    ap.add_argument("--scan", action="store_true",
                    help="run the crude beta_c susceptibility scan first")
    ap.add_argument("--seed", type=int, default=20240812)
    args = ap.parse_args()

    assert args.L % 2 == 0, "L must be even for the D_4 box"
    kinds = ["hc", "d4"] if args.lattice == "both" else [args.lattice]

    print("=" * 78)
    print("wolff_ising.py -- Ising-limit scalar on D_4 vs. hypercubic")
    print("=" * 78)

    if args.scan:
        grids = {"hc": np.arange(0.142, 0.1541, 0.002),
                 "d4": np.arange(0.042, 0.0496, 0.0015)}
        for kind in kinds:
            beta_scan(kind, args.L, grids[kind], n_therm=300, n_clusters=600,
                      seed=args.seed + 1)

    t0 = time.time()
    for kind in kinds:
        beta = args.beta if args.beta is not None else BETA_C[kind]
        run(kind, args.L, beta, args.therm, args.clusters, args.meas_every,
            args.blocks, args.seed)

    print()
    print("-" * 78)
    print("How to read the tables:")
    print("  * G(x) must be positive and decreasing in |x| on both lattices.")
    print("  * The two 'triality' pairs are a single W(F_4) orbit on D_4, so")
    print("    A(D_4) must be zero within errors while A(Z^4) is large -- the")
    print("    sharpest signature of the extra symmetry of D_4.")
    print("  * On the genuinely inequivalent pairs both lattices are")
    print("    anisotropic, but |A(D_4)| should be the smaller, increasingly")
    print("    so as |x| grows (a^4 vs. a^2 suppression).")
    print("  * Do NOT fit a power of a to two short distances in a 16^4 box;")
    print("    free_anisotropy.py does that properly in the free theory.")
    print()
    print("What a default-length run actually resolves: the triality")
    print("degeneracy, at many sigma.  The a^2-vs-a^4 hierarchy on the")
    print("genuinely inequivalent pairs is NOT resolved at L = 16 with 20k")
    print("clusters -- those A values are all consistent with zero because")
    print("the critical correlator on a small torus is almost flat over")
    print("|x| = 4-6.  Raise --clusters by an order of magnitude, or use a")
    print("larger box, before reading anything into them.")
    print(f"\ntotal wall time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()

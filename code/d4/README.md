# D_4 vs. hypercubic lattice for a scalar field — companion code

Companion code for the exercise comparing the **D_4 (four-dimensional
checkerboard) lattice** with the **hypercubic lattice Z^4** for a scalar field.

**The claim being demonstrated.** For the free lattice propagator, the leading
rotational-symmetry-breaking artifact is `O(a^2)` on the hypercubic lattice but
only `O(a^4)` on D_4. The reason is a moment identity for the 24 nearest
neighbours of D_4, the vectors `(±1,±1,0,0)` and permutations:

```
    sum_e (p.e)^2 = 12 p^2          sum_e (p.e)^4 = 12 (p^2)^2      (D_4)
    sum_e (p.e)^2 =  2 p^2          sum_e (p.e)^4 =  2 sum_mu p_mu^4  (Z^4)
```

The D_4 quartic moment is **exactly isotropic**, so the small-`p` expansion of
the kernel `Khat(p) = sum_e 2(1 - cos p.e)` is rotationally invariant through
`O(p^4)` and the first anisotropy is the `F_4`-invariant hidden in
`sum_e (p.e)^6`. On Z^4 the anisotropic `sum_mu p_mu^4` appears already at
`O(p^4)`.

Requirements: Python 3, numpy, scipy, matplotlib. No other dependencies.
All three scripts are runnable as `python3 <script>` from this directory.

---

## Files

### `d4lattice.py` — geometry and indexing library

* `d4_neighbours()` → the 24 vectors `(±1,±1,0,0)` and permutations (|e|² = 2).
* `hypercubic_neighbours()` → the 8 vectors `(±1,0,0,0)` (|e|² = 1).
* `D4Lattice(L)` / `HypercubicLattice(L)` / `make_lattice(kind, L)` — sites,
  `index(x)` and `coord(i)` maps, and an `(n_sites, q)` periodic neighbour table.
  **L must be even for D_4** (asserted): a shift by `L` must preserve the
  even-coordinate-sum condition. `n_sites = L^4/2` for D_4, `L^4` for Z^4.
* `d4_point_group()` → the 1152 elements of `W(F_4)`; `same_d4_orbit(u, v)`
  tests whether two integer vectors are related by a D_4 automorphism.

Indexing for D_4: since `sum x_i` is even, `x_4` is fixed mod 2 by
`x_1+x_2+x_3`, so with `p = (x_1+x_2+x_3) mod 2`

```
    idx = ((x_1 L + x_2) L + x_3) (L/2) + (x_4 - p)/2       in [0, L^4/2)
```

The module docstring documents the time-slice structure: fixing `x_4 = t`, the
spatial points obey `x_1+x_2+x_3 ≡ t (mod 2)`, so **every time slice is a 3d
fcc lattice** (`D_3 = A_3`) with `L^3/2` sites, successive slices being the two
interleaved fcc sublattices of `Z^3` (ABAB stacking). The 24 neighbours split
as 12 in-slice (fcc coordination 12) + 6 to `t+1` + 6 to `t−1`, so a transfer
matrix couples only adjacent slices, exactly as on the hypercubic lattice.

Run `python3 d4lattice.py` (≈ 2 s) for the self-test: shell sizes, the moment
identities above, `|W(F_4)| = 1152`, index round-trips, neighbour-table
symmetry, and the slice decomposition.

### `free_anisotropy.py` — exact free-field check (no Monte Carlo)

Computes

```
    G(x) = (1/L^4) sum_p e^{i p.x} / (Khat(p) + m^2),   p = 2 pi k / L
```

by exact summation over the L^4 discrete momenta, with the kernel normalised
so that `Khat(p) = p^2 + O(p^4)` on **both** lattices (divide the shell sum by
`c = 12` for D_4 and `c = 2` for Z^4), so `xi = 1/m` on both and the two
lattices are compared at equal physical mass. Closed forms used:

```
    Khat_hc(p) = 8 - 2 sum_mu cos p_mu
    Khat_d4(p) = (8/12) [ 6 - sum_{mu<nu} cos p_mu cos p_nu ]
```

Both kernels are even in each `p_mu` separately, so the momentum sum is done
with a **type-I DCT** over `k_mu in [0, L/2]`, sliced over the outermost
momentum. That keeps memory at `~(L/2)^3` doubles (17 MB at L = 256) instead of
the 4.3 × 10⁹ terms of the naive sum. Agreement with a direct complex FFT is
checked to 1e-14 at the start of every run.

**What is compared — and a trap.** The estimator is the pair asymmetry
`A = 2(G_a − G_b)/(G_a + G_b)` between two points of **identical** `|x|`.
The obvious axis/diagonal choices

```
    (2,0,0,0) vs (1,1,1,1)      |x|^2 = 4
    (4,0,0,0) vs (2,2,2,2)      |x|^2 = 16
```

are inequivalent on Z^4 but lie in a **single `W(F_4)` orbit on D_4**: the
triality reflection `H = ½[[1,1,1,1],[1,1,−1,−1],[1,−1,1,−1],[1,−1,−1,1]]`
maps `(r,0,0,0) → (r/2,r/2,r/2,r/2)`. On D_4 `G` is therefore *exactly* equal
on them and the asymmetry vanishes for a trivial symmetry reason — it says
nothing about the order of the artifact. Part 1 of the script prints this
explicitly (A(D_4) = 1e-16 …1e-14 = round-off).

The smallest D_4 shell carrying **two** distinct `W(F_4)` orbits is
`|x|^2 = 18` (orbit sizes 24 and 288), so the scan uses the scalable pair

```
    x_a = lam (3,3,0,0)     x_b = lam (4,1,1,0)     |x| = lam sqrt(18)
```

Both have even coordinate sum for every `lam`, so both exist on D_4 *and* on
Z^4, and their multisets of |coordinates| differ, so they are inequivalent
under `B_4` as well.

**How the power is extracted.** Varying `m` at fixed lattice separation does
*not* measure the order of the artifact — for `xi >> |x|` the asymmetry
saturates at the mass-independent short-distance value. The continuum limit is
`a → 0` at fixed physical separation and mass, i.e. `|x|` and `xi` must grow
together with `rho = |x|/xi` held fixed (default `rho = 2.5`). Then
`|A| = C (1/xi)^n` with `n = 2` (Z^4) and `n = 4` (D_4).

Output: a table of `G_a`, `G_b`, `A`; successive local slopes; power-law fits;
a finite-volume cross-check at `L = 192` vs `L = 256`; and the figure
`anisotropy.pdf` / `anisotropy.png` (house style
`/home/user/lqft-book/figures/src/lqftbook.mplstyle`, curves direct-labelled,
no legend box).

```
python3 free_anisotropy.py                    # L = 256, ~2 min
python3 free_anisotropy.py --L 128 --lam-max 5 --no-plot   # ~6 s
python3 free_anisotropy.py --rho 2.0 --drop 1
```

### `wolff_ising.py` — Wolff single-cluster MC on both lattices

Ising limit `S = −beta sum_<ij> s_i s_j`, `s = ±1`, using the neighbour tables
from `d4lattice.py`. Standard single-cluster growth with
`p_add = 1 − exp(−2 beta)`, vectorised shell by shell. Cold (ordered) start:
from a random configuration the Wolff branching ratio at `beta_c` is only
`~(q−1) p_add / 2 ≈ 1` and the chain effectively does not thermalise.

`G(x)` is measured for **all** separations at once by embedding the spins in
the full `L^4` grid (zeros on odd-sum sites for D_4) and taking the FFT
autocorrelation, `G(x) = irfftn(|rfftn(s)|^2) / N_sites`. Errors are jackknife
over 25 blocks, applied to the ratio `A` itself so the strong `G_a`–`G_b`
correlation is handled correctly.

```
python3 wolff_ising.py               # L=16, 2000 therm + 20000 clusters, ~50 s
python3 wolff_ising.py --scan        # + crude beta_c susceptibility scan, ~30 s more
python3 wolff_ising.py --clusters 200000 --lattice d4
```

---

## Where to sit near criticality

| lattice | q | mean field `1/q` | value used | source |
|---|---|---|---|---|
| Z^4 | 8 | 0.1250 | **0.149695** | literature 4d Ising `beta_c` |
| D_4 | 24 | 0.041667 | **0.0457 ± ~0.0010** | measured here, Binder crossing |

`beta_c(D_4)` was obtained from Binder-cumulant crossings
`U_L = 1 − <m^4>/(3<m^2>^2)` between `L = 8` and `L = 12`, 9000 clusters per
point:

| beta | U(L=8) | U(L=12) |
|---|---|---|
| 0.0450 | 0.277(25) | 0.195(35) |
| 0.0455 | 0.389(19) | 0.326(35) |
| 0.0460 | 0.466(12) | 0.545(11) |

crossing near `beta = 0.0457`. This is a **crude** two-volume estimate, not a
determination. The cheaper `--scan` (susceptibility crossing `chi = L^2`, the
`eta = 0` finite-size value) gives 0.1486 for Z^4 and 0.0450 for D_4 — both
undershoot by 1–2 %, consistent with each other.

---

## Results actually obtained

### Free field (`free_anisotropy.py`, L = 256, rho = 2.5)

Part 1 — the triality trap (L = 64, xi = 2):

| pair | \|x\|² | same W(F_4) orbit | A (Z^4) | A (D_4) |
|---|---|---|---|---|
| (2,0,0,0) vs (1,1,1,1) | 4 | yes | +5.53e−01 | −2.5e−16 |
| (4,0,0,0) vs (2,2,2,2) | 16 | yes | +2.92e−01 | +1.1e−14 |
| (3,3,0,0) vs (4,1,1,0) | 18 | no | −6.27e−02 | +2.32e−02 |
| (6,0,0,0) vs (4,4,2,0) | 36 | no | +1.51e−01 | −6.98e−03 |

Part 2 — the continuum-limit scan:

| lam | \|x\| | xi | A (Z^4) | A (D_4) |
|---|---|---|---|---|
| 1 | 4.243 | 1.697 | −7.347e−02 | +2.893e−02 |
| 2 | 8.485 | 3.394 | −2.579e−02 | +1.427e−03 |
| 3 | 12.728 | 5.091 | −1.196e−02 | +2.731e−04 |
| 4 | 16.971 | 6.788 | −6.821e−03 | +8.564e−05 |
| 5 | 21.213 | 8.485 | −4.392e−03 | +3.494e−05 |
| 6 | 25.456 | 10.182 | −3.060e−03 | +1.682e−05 |

Local two-point slopes `d log|A| / d log(1/xi)`:

```
    Z^4 :  1.510  1.894  1.953  1.973  1.982      -> 2
    D_4 :  4.341  4.078  4.031  4.017  4.011      -> 4
```

**Fitted exponents** `|A| = C (1/xi)^n`:

| lattice | n (all 6 points) | n (drop 2 coarsest) | expected |
|---|---|---|---|
| hypercubic Z^4 | 1.788 | **1.967** | 2 |
| D_4 | 4.149 | **4.022** | 4 |

The residual deviation from 2 and 4 is the expected subleading `O(a^2)`
correction to each leading term, and it shrinks monotonically along the local
slopes. Finite volume is under control: the largest-`xi` point drifts by
2.8e−06 (Z^4) and 5.2e−04 (D_4) between `L = 192` and `L = 256`, both far
below the signal. The cheap mode `--L 128 --lam-max 5` gives 1.961 and 4.059
in 6 s — same conclusion, and its own `L = 96` cross-check makes the
finite-volume systematic visible (the D_4 point at `xi = 8.5` moves by 280 %
between `L = 96` and `L = 128`, which is exactly why the default is 256).

Figure: `anisotropy.pdf`, `anisotropy.png`.

### Monte Carlo (`wolff_ising.py`, L = 16, 20000 clusters, at `beta_c`)

Hypercubic, `beta = 0.149695`, `<|C|> = 705` (1.1 % of the lattice),
`<|m|> = 0.0908(39)`:

| pair | \|x\| | G(x_a) | G(x_b) | A | A (m² subtracted) |
|---|---|---|---|---|---|
| (2,0,0,0) vs (1,1,1,1) | 2.000 | 0.058686(743) | 0.042008(875) | **+0.3312(115)** | +0.4236(123) |
| (4,0,0,0) vs (2,2,2,2) | 4.000 | 0.017782(789) | 0.017078(775) | +0.0404(172) | +0.1091(475) |
| (3,3,0,0) vs (4,1,1,0) | 4.243 | 0.016210(828) | 0.016245(823) | −0.0022(264) | −0.0067(814) |
| (6,0,0,0) vs (4,4,2,0) | 6.000 | 0.012605(768) | 0.012367(790) | +0.0191(338) | +0.1583(2847) |

D_4, `beta = 0.0457`, `<|C|> = 759` (2.3 %), `<|m|> = 0.1371(46)`:

| pair | \|x\| | G(x_a) | G(x_b) | A | A (m² subtracted) |
|---|---|---|---|---|---|
| (2,0,0,0) vs (1,1,1,1) | 2.000 | 0.059269(1020) | 0.059736(938) | **−0.0078(64)** | −0.0127(103) |
| (4,0,0,0) vs (2,2,2,2) | 4.000 | 0.029506(1238) | 0.029337(1046) | +0.0057(131) | +0.0255(588) |
| (3,3,0,0) vs (4,1,1,0) | 4.243 | 0.028328(1125) | 0.028563(1226) | −0.0082(115) | −0.0415(587) |
| (6,0,0,0) vs (4,4,2,0) | 6.000 | 0.024907(1079) | 0.024471(1251) | +0.0177(151) | +0.2320(1890) |

`G(x)` is positive and monotonically decreasing in `|x|` on both lattices, the
cluster sizes are a sensible few per cent of the volume at `beta_c`, and the
jackknife errors scale as `1/sqrt(N)` between the short test runs and the
production run.

**What this run does and does not show, honestly.**

* It **does** resolve the triality degeneracy at high significance: on the
  `(2,0,0,0)` vs `(1,1,1,1)` pair, `A(Z^4) = +0.331(12)` (≈ 29 sigma from
  zero) while `A(D_4) = −0.008(6)` (consistent with zero). That is the exact
  `W(F_4)` symmetry of D_4 showing up in interacting Monte Carlo data.
* It **does not** resolve the `a^2` vs `a^4` hierarchy on the genuinely
  inequivalent pairs. At `L = 16` and `beta_c` the correlator is nearly flat
  over `|x| = 4…6` — on a torus `sum_x G(x) = M^2/N`, so `G(x)` sits on an
  `x`-independent pedestal `<m^2>` (≈ 0.011 on Z^4, ≈ 0.023 on D_4) that is
  comparable to `G` itself at those distances and dilutes the ratio. All four
  `A` values on those pairs are within ~1.5 sigma of zero on both lattices, and
  the corresponding free-field values at `xi = 2` (−0.063 on Z^4 and +0.023 on
  D_4 at `|x|^2 = 18`) sit at or below the achievable resolution. Order-of-magnitude more statistics, or a larger
  box, would be needed. **Extracting the exponents is the job of
  `free_anisotropy.py`, not of this short run.**
* The periodic torus itself breaks triality (`H` maps `(L,0,0,0)` to
  `(L/2,L/2,L/2,L/2)`, not in `L Z^4`) by `O(exp(−L/2 xi))`, which at
  criticality on `L = 16` is not parametrically small. A small nonzero `A` on
  the D_4 triality pairs would therefore be a boundary-condition effect and not
  a lattice artifact.

---

## Runtimes (2 cores)

| command | wall time |
|---|---|
| `python3 d4lattice.py` | 2 s |
| `python3 free_anisotropy.py` (L = 256) | 112 s |
| `python3 free_anisotropy.py --L 128 --lam-max 5 --no-plot` | 6 s |
| `python3 wolff_ising.py` | 50 s |
| `python3 wolff_ising.py --scan` | + 28 s |

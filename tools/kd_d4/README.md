# Kähler–Dirac fermions on `D_4`

Backs the remark at the end of §"Geometric interpretation of DK fermions"
(`chapters/ch06-lattice-fermions/staggered.tex`).

    python3 complex.py                 # build both complexes, check ∂² = 0
    python3 hodge_weights.py           # derive w_p from the dual-cell volumes
    python3 kd_spectrum.py [--scan]    # the spectrum table (--scan is slow)

## What is built

`complex.py` constructs the Delaunay complex of `D_4` — the **16-cell
honeycomb** — as a translation-invariant chain complex, together with the
ordinary cubical complex on `Z^4` for comparison, and returns Bloch
(momentum-space) boundary operators.

| | 0 | 1 | 2 | 3 | 4 | total |
|---|---|---|---|---|---|---|
| `Z^4` | 1 | 4 | 6 | 4 | 1 | 16 |
| `D_4` | 1 | 12 | 32 | 24 | 3 | 72 |

The 4-cells of `D_4` are 16-cells centred on the deep holes: one orbit at the
odd `Z^4` points, two at the half-integer points, `1 + 2 = 3` per site. Their
boundary is `∂ = Σ_s (Π s_i) [h + s_1 u_1, …, h + s_4 u_4]`, the cross-polytope
formula; `∂² = 0` is checked numerically, which is the real test of the
orientation conventions.

## What is found

* **Harmonic cochains** at `k = 0` come out as `1,4,6,4,1` on *both* lattices —
  the Betti numbers of `T^4`, as Hodge theory requires. So the exterior algebra
  is recovered exactly on `D_4`, out of a 72-dimensional space.
* The **circumcentric Hodge star** `w_p = |*σ|/|σ| = (2, 1/3, 1/2, 3, 3/2)` is
  essential. With the naive orthonormal inner product the 16 light modes split
  into four velocities `√6, 2/√6, 1/√6, √2` by form degree; with `w_p` they are
  all exactly `1`.
* **No doublers**: the only zero of `d − δ` in the Brillouin zone is at `k = 0`.
  The other 56 branches never fall below `2√2` in lattice units.
* **Isotropic `O(a²)`**: `|λ|/|k| = 1 − |k|²/64 + O(k⁴)`, the same in every
  direction. On `Z^4` the coefficient is `−Σ_μ k̂_μ⁴/24`, a factor of four
  between the axis and the body diagonal. This is the no-quartic-`F_4`-invariant
  story of Ch. 3 showing up in the fermion dispersion.
* `Γ = (−1)^p` anticommutes with `d − δ` on any complex, so the `U(1)`
  Kähler–Dirac chiral symmetry is untouched.

## What does *not* work

Both steps of the textbook construction are hypercubic:

* the Kawamoto–Smit rotation needs the product of `γ`'s around every closed loop
  to be a multiple of the identity — true for the 12 hypercubic plaquettes, false
  for all 96 `D_4` triangles;
* the Dirac–Kähler identification needs `binom(4,p) = 1,4,6,4,1` cells per site,
  i.e. a hypercubic vertex figure. `72/16` is not an integer.

See `d4_verify.py`, `d4_verify2.py` and `d4_minimal_doubling.py` in `tools/`
for the rest of the `D_4` thread.

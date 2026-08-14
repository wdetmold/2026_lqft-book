# The $D_4$ problem thread

A running sequence of exercises developing lattice field theory on the
four-dimensional checkerboard lattice $D_4$, threaded through the foundational
chapters. Each chapter's instalment stands alone but builds on the last.

**The organising idea.** $\mathrm{Aut}(D_4) = W(F_4)$ has order 1152, three
times the hypercubic group, and its polynomial invariants have degrees
2, 6, 8, 12 — with *no* independent quartic invariant. Everything else in the
thread is a consequence: isotropic $\mathcal{O}(a^2)$ artifacts for any action,
rotational-symmetry breaking postponed to $\mathcal{O}(a^4)$, exact degeneracies
among lattice sites, fewer free parameters in improvement programmes, and a
minimally doubled fermion with an unusually good free spectrum.

## Status

| Chapter | Instalment | Status |
|---|---|---|
| 2 Path integrals | geometry of $D_d$; the dual and isoduality; the 24-cell and $W(F_4)$ | **drafted** (3 exercises, figures live here) |
| 3 Scalar fields | geometry; free propagator; $F_4$ invariants; triality degeneracy; numerics; transfer matrix & RP; Symanzik improvement; hopping expansion | **drafted** (8 exercises, `exercises-d4.tex`) |
| 4 Gauge fields | triangular plaquette action; no checkerboard but a three-octant decomposition; rectangle improvement | **drafted** (2 exercises) |
| 5 Hamiltonian LGT | Kogut–Susskind limit with no straight temporal bond | planned |
| 6 Lattice fermions | minimally doubled fermions (Borići–Creutz $=$ Karsten–Wilczek on $D_4$); free $\slashed{D}$ spectrum; doubler count | planned |
| 7 Improvement | $\mathcal{O}(a)$ improvement, continuing Ch. 3's counting | planned |
| 8 Monte Carlo | pure-gauge transfer matrix; bulk phase transition | planned |

## Chapter 3 — drafted

1. **Geometry.** Shells (24, 24, 96); $\mathrm{BCH}_d \cong D_d$ only for $d=4$
   (connects to the existing general-$d$ BCH problem); non-bipartite, 96
   triangles per site; alternating fcc time slices, no straight temporal bond.
2. **Free propagator.** $\sum_e (p\cdot e)^2 = 12p^2$, $\sum_e (p\cdot e)^4 =
   12(p^2)^2$ — the anisotropic $\sum_\mu p_\mu^4$ cancels identically.
3. **Invariant theory.** $H \in \mathrm{Aut}(D_4)$ with half-integer entries;
   degrees 2, 6, 8, 12; corollary that *every* $D_4$ action has isotropic
   $\mathcal{O}(a^2)$ artifacts; the degree-6 invariant $J_6$.
4. **Triality degeneracy.** $G(2,0,0,0) = G(1,1,1,1)$ exactly; shells
   $|x|^2 \le 16$ are single orbits, so $G$ depends only on $|x|$ that far; the
   first split is at $|x|^2 = 18$.
5. **Numerical project.** Free-field anisotropy exponent (2 vs 4) and the
   Monte Carlo degeneracy test; includes two instructive traps.
6. **Transfer matrix.** $T$ maps between sublattices so $T^2$ is the object;
   site reflection is an automorphism, link reflection is not; positivity
   requires $\sum_i \cos p_i > 0$.
7. **Symanzik improvement.** Second shell is one orbit → one coupling;
   $c_1 = 1/6$, $c_2 = -1/24$.
8. **Hopping expansion.** $\kappa_c = 1/48$; closed-walk counts with odd terms
   present; $1/q$ suppression of mean-field error.

## Gauge-theory figures (Chapter 4)

`fig-d4-links` and `fig-d4-plaquettes` are drafted and placed in
`chapters/ch04-gauge-fields/exercises-d4.tex`, with a `\todo` marking the
exercises still to be written. Verified counts behind them:

| | $D_4$ | $\mathbb{Z}^4$ |
|---|---|---|
| independent link directions per site | 12 | 4 |
| 3-link loops through a site | 96 (32 per site) | 0 (bipartite) |
| 4-link loops through a site | 936 | 24 |
| of which planar rhombi | 264 (72 right-angled) | 24 |

The reading that makes the figures work: a chord between two neighbours of a
site exists exactly when those neighbours are themselves linked, so the 96
edges of the 24-cell *are* the 96 elementary triangles through that site. The
same construction on $\mathbb{Z}^4$ yields no chords at all.

## New results established while drafting

- **Three-octant decomposition.** The 24 link directions split into three
  classes of eight, by the three pairings of the coordinate axes:
  A = (12),(34); B = (13),(24); C = (14),(23). Two vectors of one class never
  sum to a minimal vector, so each of the 96 triangles carries exactly one link
  per class. Hence a three-sweep parallel update that, unlike the hypercubic
  checkerboard, needs no site parity. $\mathrm{Aut}(D_4)$ permutes the classes
  as $S_3 = \mathrm{Aut}(D_4)/W(D_4)$ — precisely triality.
- **Gamma matrices on links.** $\gamma_e = (\gamma_\mu \pm \gamma_\nu)/\sqrt2$
  satisfies $\gamma_e^2 = 1$, so half-spinor projectors survive with rank 2.
  But $\{\gamma_e,\gamma_f\} = (e\cdot f)\mathbb{1}$, and triangle-sharing
  links have $e\cdot f = 1$: they neither commute nor anticommute, so the
  hypercubic sign-flip implementation of spin projection does not carry over.
- **Naive doubling.** 72 nondegenerate zeros in the Brillouin zone, of which
  only 16 are the familiar half-period points; the other 56 sit at generic
  momenta such as $(\pi/3,\pi/3,\pi/3,\pi)$ (verified by hand as well as
  numerically). Against $\mathbb{Z}^4$'s 16.
- **Minimal doubling: KW = BC on $D_4$** (author's result). The
  Karsten--Wilczek direction $(2,0,0,0)$ and the Borici--Creutz direction
  $(1,1,1,1)$ are inequivalent under the hypercubic group but lie in a *single*
  $\mathrm{Aut}(D_4)$ orbit — the second shell — so on $D_4$ the two
  constructions are related by a lattice symmetry. Numerically both leave
  exactly **2** nondegenerate zeros, for every coupling tested
  (`tools/d4_minimal_doubling.py`). One term removes 70 of 72 zeros, because
  the extra naive zeros come in orbits and are lifted wholesale.
  *This is the same triality degeneracy that gives $G(2,0,0,0)=G(1,1,1,1)$
  exactly in Ch.3 and the three octants in Ch.4.*
- **Antiperiodic boundary conditions.** All temporal links have
  $|\Delta t| = 1$, so one uniform phase suffices; triangles come only in
  $\Delta t$ patterns $(0,0,0)$ and $(+1,-1,0)$, both flat. The root
  convention is *simpler* than the body-centred one here, where the axial link
  spans two time levels.

## Verified inputs

All numerical and algebraic claims in the solutions were checked:
$|\mathrm{Aut}(D_4)| = 1152$ by brute-force enumeration; the Molien series
matches $\prod_{d \in \{2,6,8,12\}} (1-t^d)^{-1}$ exactly; shell orbit
decompositions; 96 triangles; closed-walk counts 24, 192, 3384, 51840 ($D_4$)
against 8, 0, 168, 0 ($\mathbb{Z}^4$); improvement couplings; free-field
anisotropy exponents 1.97 and 4.02; Monte Carlo $A(\mathbb{Z}^4) = +0.331(12)$
against $A(D_4) = -0.008(6)$.

## Draft flags

All eight exercises are marked `\problemdraft`, so each prints an "unverified
draft — author check pending" tag in the PDF until you clear it. Accept one by
deleting `draft` from the command name (and any `[note]`). Two specific claims
are additionally wrapped in `\unverified{...}`. Run
`python3 tools/list_draft_flags.py` for the live checklist.

## Open items for the author

- $\beta_c(D_4)$ is currently a crude $16^4$ Binder crossing, $0.0457(10)$. A
  proper finite-size-scaling determination would firm up Exercise 8(c) — and is
  a good student project in its own right.
- Exercise 6(d) asserts that $T^2$ is positive while $T$ need not be. The
  argument given is the standard site-reflection one; worth a second look
  before the solutions manual is published.
- Consider whether the thread wants a short in-text box in Ch. 3 introducing
  $D_4$, so the exercises are not the reader's first encounter with it.

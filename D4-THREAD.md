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
| 3 Scalar fields | geometry; free propagator; $F_4$ invariants; triality degeneracy; numerics; transfer matrix & RP; Symanzik improvement; hopping expansion | **drafted** (8 exercises, `exercises-d4.tex`) |
| 4 Gauge fields | Wilson action on $D_4$; triangle and rectangle plaquettes; improvement parameter counting from $F_4$ orbits | planned |
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

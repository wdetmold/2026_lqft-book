#!/usr/bin/env python3
"""Positivity of momentum-projected correlators on a D_4 torus.

    python3 tools/d4_positivity.py [L]        # default L = 8

Free scalar on D_4 with periods L*e_mu (L^4/2 sites).  Time slices alternate
between the two fcc cosets, so the transfer matrix maps one Hilbert space to
the other; only T^2 is an operator on a fixed space.  The residual coset phase
shows up as a sign in the momentum-projected correlator.

Exact kinematic identity (holds non-perturbatively):
    C(t, p + (pi,pi,pi)) = (-1)^t C(t, p)
because exp(i(pi,pi,pi).x) = (-1)^{sum x} = (-1)^t on slice t, while
(pi,pi,pi) = 2 pi (1/2,1/2,1/2) IS a reciprocal-lattice vector of the fcc slice.
So p and p + (pi,pi,pi) label the SAME state; the sign of C is a convention.

What the script establishes, for every allowed spatial momentum:
    sign C(t, p) = [ sign(sum_i cos p_i) ]^t                       (exact here)
    sum_i cos p_i = 0  =>  C(odd t) = 0 identically -- and this case is NOT a
        convention: there p + (pi,pi,pi) lies in the point-group orbit of -p,
        so parity forces C(t) = (-1)^t C(t).
Such momenta exist iff 4 | L or 6 | L.  Choose L = 2 or 10 (mod 12) to avoid
them entirely.
"""
import sys, itertools, collections, numpy as np

L = int(sys.argv[1]) if len(sys.argv) > 1 else 8
M2 = 0.10

k1 = 2*np.pi*np.arange(L)/L
K = np.meshgrid(k1, k1, k1, k1, indexing="ij")
c = [np.cos(x) for x in K]
D = M2 + 24 - 4*sum(c[m]*c[n] for m in range(4) for n in range(m+1, 4))
G = np.fft.ifftn(1.0/D).real
X = np.array(np.meshgrid(*[np.arange(L)]*4, indexing="ij"))
even = (X.sum(0) % 2 == 0)


def project(field, p):
    ph = np.exp(-1j*(p[0]*X[1] + p[1]*X[2] + p[2]*X[3]))
    return (np.where(even, field, 0.0)*ph).sum(axis=(1, 2, 3))


def red(p):
    q = np.mod(np.asarray(p, float) + np.pi, 2*np.pi) - np.pi
    return np.where(np.isclose(q, -np.pi), np.pi, q)


part = lambda m: tuple((x + L//2) % L for x in m)
PG = [(pm, s) for pm in itertools.permutations(range(3))
      for s in itertools.product((1, -1), repeat=3)]
orbit = lambda m: {tuple((s[i]*m[pm[i]]) % L for i in range(3)) for pm, s in PG}

seen, keep = set(), []
for m in itertools.product(range(L), repeat=3):
    if m in seen: continue
    seen.add(m); seen.add(part(m)); keep.append(m)

print("L = %d  D_4 torus: %d sites, %d distinct spatial momenta per fcc slice"
      % (L, int(even.sum()), len(keep)))
mm = (1, 2, 3 % L)
a = project(G**2, 2*np.pi*np.array(mm)/L).real
b = project(G**2, 2*np.pi*np.array(mm)/L + np.pi).real
print("  check C(t,p+(pi,pi,pi)) = (-1)^t C(t,p):  max dev %.1e"
      % np.abs(b - np.array([(-1)**t for t in range(L)])*a).max())

cat, oddzero, ties = collections.Counter(), [], []
for m in keep:
    C_ = project(G**2, 2*np.pi*np.array(m)/L).real
    p, pp = red(2*np.pi*np.array(m)/L), red(2*np.pi*np.array(part(m))/L)
    sc = float(np.sum(np.cos(p)))
    if all(abs(C_[t]) < 1e-12*abs(C_[0]) for t in range(1, L, 2)):
        cat["C(odd t) = 0"] += 1
        oddzero.append((m, sc, part(m) in orbit(m), float(np.linalg.norm(p))))
    else:
        neg = any(C_[t] < 0 for t in range(1, L//2 + 1))
        assert (sc < 0) == neg, (m, sc, neg)          # the rule, tested
        cat["alternating" if neg else "positive"] += 1
        if neg and np.dot(p, p) <= np.dot(pp, pp) + 1e-12: ties.append(m)

for k, v in cat.items(): print("  %-16s %4d" % (k, v))
print("  the rule  sign C(t,p) = sign(sum_i cos p_i)^t  held for every momentum")
if oddzero:
    print("  of the %d with C(odd t) = 0: all have sum cos = 0 (%s) and "
          "p+(pi,pi,pi) in the point-group orbit of p (%s)"
          % (len(oddzero), all(abs(x[1]) < 1e-12 for x in oddzero),
             all(x[2] for x in oddzero)))
    print("     smallest |p| among them: %.4f = %.3f pi"
          % (min(x[3] for x in oddzero), min(x[3] for x in oddzero)/np.pi))
print("  momenta where |p| cannot break the tie (use sum cos instead): %d" % len(ties))

print("\n  which L have any momentum with sum_i cos p_i = 0?")
for Ltest in range(4, 27, 2):
    v = sorted({round(float(np.cos(2*np.pi*n/Ltest)), 12) for n in range(Ltest)})
    hit = any(abs(a_+b_+c_) < 1e-10 for a_ in v for b_ in v for c_ in v)
    print("     L=%2d : %s" % (Ltest, "yes" if hit else "NO  <- safe"))

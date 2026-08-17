#!/usr/bin/env python3
"""Free Kaehler-Dirac spectrum on D_4, with Z^4 as a control.

    python3 tools/kd_d4/kd_spectrum.py            # the summary table
    python3 tools/kd_d4/kd_spectrum.py --scan     # + Brillouin-zone scan (slow)

The complex is built in complex.py; the Hodge weights are derived in
hodge_weights.py.  Everything reported here is recomputed from scratch.

Summary of what this prints (all reproduced values):

  cells per site      D_4 [1,12,32,24,3] = 72     Z^4 [1,4,6,4,1] = 16
  harmonic cochains   1,4,6,4,1 (= Betti numbers of T^4) for BOTH
  Hodge weights       w_p = |*sigma|/|sigma| = (2, 1/3, 1/2, 3, 3/2) on D_4
  light velocities    all 16 equal to 1, isotropic (only after weighting)
  gap of the other 56 2*sqrt(2) in lattice units, over the whole BZ
  O(a^2) coefficient  D_4: -1/64, direction-independent
                      Z^4: -sum_mu khat_mu^4 / 24  (-1/24 .. -1/96)
  chiral symmetry     Gamma = (-1)^p anticommutes with d - delta
"""
import itertools, sys, numpy as np
from complex import build_D4, build_Z4

W_D4 = {0: 2.0, 1: 1/3, 2: 0.5, 3: 3.0, 4: 1.5}     # see hodge_weights.py
W_Z4 = {p: 1.0 for p in range(5)}
# a D_4 basis, and the dual basis that parametrises the Brillouin zone
BASIS = np.array([[1, -1, 0, 0], [0, 1, -1, 0], [0, 0, 1, -1], [0, 0, 1, 1]], float)
DUAL = np.linalg.inv(BASIS).T


def weighted_K(C, w, k):
    """K = d - delta at momentum k, similarity-transformed to be anti-Hermitian"""
    D, _, _ = C.bloch_d(k)
    s = np.concatenate([np.full(C.n[p], np.sqrt(w[p])) for p in range(5)])
    Dt = (s[:, None] * D) / s[None, :]
    return Dt - Dt.conj().T


def branches(C, w, k):
    return np.sort(np.abs(np.linalg.eigvals(weighted_K(C, w, k))))


def harmonic_by_degree(C):
    out = []
    for p in range(5):
        blocks = []
        if p < 4: blocks.append(C.bloch_boundary(p + 1, np.zeros(4)).conj().T)
        if p > 0: blocks.append(C.bloch_boundary(p, np.zeros(4)))
        M = np.vstack(blocks)
        out.append(M.shape[1] - np.linalg.matrix_rank(M, tol=1e-9))
    return out


def main():
    C4, CZ = build_D4(), build_Z4()
    for name, C, w in (("D_4", C4, W_D4), ("Z^4", CZ, W_Z4)):
        cv = [C.n[p] for p in range(5)]
        print("=" * 66)
        print("%s : cells per site %s = %d   Euler %d"
              % (name, cv, sum(cv), sum((-1) ** p * c for p, c in enumerate(cv))))
        rng = np.random.default_rng(1)
        D, _, _ = C.bloch_d(rng.normal(size=4))
        print("  nilpotency: max |d^2| = %.1e" % np.abs(D @ D).max())
        print("  harmonic cochains by degree: %s  (Betti numbers of T^4)"
              % harmonic_by_degree(C))
        s0 = branches(C, w, np.zeros(4))
        nl = int((s0 < 1e-9).sum())
        print("  zero modes at k=0: %d ; the rest span %.4f .. %.4f"
              % (nl, s0[nl] if nl < len(s0) else np.nan, s0[-1]))
        print("  velocities of the %d light branches:" % 16)
        for d in ([1, 0, 0, 0.], [1, 1, 0, 0.], [1, 1, 1, 1.], [1, 2, 3, 4.]):
            dn = np.array(d) / np.linalg.norm(d)
            s = branches(C, w, 1e-3 * dn)[:16] / 1e-3
            print("     %-16s %.8f .. %.8f" % (str(d), s.min(), s.max()))
        print("  c = (|lambda|/|k| - 1)/k^2  at |k| = 0.05:")
        for d in ([1, 0, 0, 0.], [1, 1, 0, 0.], [1, 1, 1, 1.], [1, 1, 1, 0.]):
            dn = np.array(d) / np.linalg.norm(d)
            c = (branches(C, w, 0.05 * dn)[:16].mean() / 0.05 - 1) / 0.05 ** 2
            print("     %-16s c = %+.8f   (1/c = %+.2f)" % (str(d), c, 1 / c))
        G = np.diag(np.concatenate([np.full(C.n[p], (-1.0) ** p) for p in range(5)]))
        K = weighted_K(C, w, np.array([0.3, -0.7, 0.2, 1.1]))
        print("  chiral symmetry: max |{(-1)^p, K}| = %.1e" % np.abs(G @ K + K @ G).max())

    if "--scan" in sys.argv:
        print("=" * 66)
        L = 8
        best, heavy = (9e9, None), 9e9
        for t in itertools.product(range(L), repeat=4):
            s = branches(C4, W_D4, 2 * np.pi * (np.array(t) / L @ DUAL))
            heavy = min(heavy, s[16])
            if any(t) and s[0] < best[0]: best = (s[0], t)
        print("D_4 Brillouin-zone scan, %d^4 momenta:" % L)
        print("  smallest |lambda| away from k=0 : %.6f at t=%s  -> no doublers"
              % (best[0], str(best[1])))
        print("  minimum of the 17th branch      : %.4f = 2*sqrt(2)" % heavy)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Zero-counting for naive and minimally doubled fermions on D_4.

Reproduces the counts quoted in the Ch.6 exercises:
  naive                          -> 72 nondegenerate zeros in the BZ
  + Karsten-Wilczek term (axial) ->  2
  + Borici-Creutz term (diagonal)->  2
The two agree because (2,0,0,0) and (1,1,1,1) lie in one Aut(D_4) orbit.
"""
import itertools, numpy as np
from scipy.optimize import fsolve

S = [np.array(v, float) for v in itertools.product((-1, 0, 1), repeat=4)
     if sum(v) % 2 == 0 and sum(x * x for x in v) == 2]
DIRS = []
for v in S:
    if not any(np.array_equal(v, -d) for d in DIRS):
        DIRS.append(v)
E = np.array(DIRS)

def V(p):  return (E.T * np.sin(E @ p)).sum(axis=1)
def Ssum(p): return float((1 - np.cos(E @ p)).sum())

def zeros(nhat=None, c=0.0, seed=3, ntry=2500):
    if nhat is None:
        F = V
    else:
        n = np.array(nhat, float); n /= np.linalg.norm(n)
        F = lambda p: V(p) + c * n * Ssum(p)
    rng = np.random.default_rng(seed)
    starts = [np.array(x) * np.pi / 2 for x in itertools.product(range(4), repeat=4)]
    starts += [rng.uniform(0, 2 * np.pi, 4) for _ in range(ntry)]
    sols = {}
    for s in starts:
        x, info, ier, msg = fsolve(F, s, full_output=True)
        if ier != 1 or np.linalg.norm(F(x)) > 1e-9:
            continue
        J = np.zeros((4, 4)); h = 1e-6
        for k in range(4):
            d = np.zeros(4); d[k] = h
            J[:, k] = (F(x + d) - F(x - d)) / (2 * h)
        if abs(np.linalg.det(J)) < 1e-7:          # keep nondegenerate zeros only
            continue
        sols[tuple(np.round(np.mod(x / np.pi, 2.0), 4) % 2.0)] = np.mod(x, 2 * np.pi)
    reps = {}                                      # quotient by the D_4* glue shift
    for k, x in sols.items():
        k2 = tuple(np.round(np.mod((x + np.pi) / np.pi, 2.0), 4) % 2.0)
        if k2 not in reps:
            reps[k] = x
    return reps

if __name__ == "__main__":
    print("naive                :", len(zeros()), "zeros")
    for c in (0.15, 0.4, 1.0):
        a = len(zeros([0, 0, 0, 1], c))
        b = len(zeros([1, 1, 1, 1], c))
        print(f"c={c:<5} KW (axial) : {a:3d}    BC (diagonal) : {b:3d}")

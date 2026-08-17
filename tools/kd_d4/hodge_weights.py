"""Circumcentric (DEC) Hodge weights for the Delaunay complex of D_4.

For a p-cell sigma, the dual (4-p)-cell is the convex hull of the circumcentres
of the 4-cells containing sigma -- and the circumcentre of a 16-cell IS its
deep hole.  The Hodge weight is w_p(sigma) = |dual sigma| / |sigma|.
"""
import itertools, math, numpy as np
from fractions import Fraction
from scipy.spatial import ConvexHull

D4 = set(v for v in itertools.product(range(-4, 5), repeat=4) if sum(v) % 2 == 0)
MIN = [v for v in D4 if sum(x*x for x in v) == 2]
holes = [np.array([1.0 if i == m else 0.0 for i in range(4)])*s
         for m in range(4) for s in (1, -1)]
holes += [np.array(s, float)/2 for s in itertools.product((1, -1), repeat=4)]
# all holes within reach (need holes around any cell, not just around 0)
ALLH = []
for h0 in itertools.product(range(-4, 5), repeat=4):
    if sum(h0) % 2 == 1: ALLH.append(np.array(h0, float))
for h0 in itertools.product([x/2 for x in range(-7, 8, 2)], repeat=4):
    ALLH.append(np.array(h0, float))
ALLH = np.array(ALLH)

def dual_of(verts):
    v0 = np.array(verts[0], float)
    d = np.linalg.norm(ALLH - v0, axis=1)
    cand = ALLH[np.abs(d - 1) < 1e-9]
    for v in verts[1:]:
        d = np.linalg.norm(cand - np.array(v, float), axis=1)
        cand = cand[np.abs(d - 1) < 1e-9]
    return cand

def vol(points, dim):
    P = np.atleast_2d(points)
    if dim == 0: return 1.0
    c = P.mean(0); Q = P - c
    U, S, Vt = np.linalg.svd(Q, full_matrices=False)
    basis = Vt[:dim]
    R = Q @ basis.T
    if dim == 1: return float(R.max() - R.min())
    return float(ConvexHull(R).volume)

def simp_vol(verts, p):
    V = np.array(verts, float)
    M = V[1:] - V[0]
    G = M @ M.T
    return float(np.sqrt(abs(np.linalg.det(G)))/math.factorial(p))

# ---- representative cells
def cliques(k):
    return [c for c in itertools.combinations(MIN, k)
            if all(sum(a*b for a,b in zip(c[i],c[j])) == 1
                   for i in range(k) for j in range(i+1,k))]
reps = {0: [[(0,0,0,0)]]}
for p in (1,2,3):
    reps[p] = [[(0,0,0,0)]+list(c) for c in cliques(p)]
# 4-cells: the 16-cells around the origin
reps[4] = None

print("Hodge weights w_p = |dual| / |cell|   (circumcentric / DEC)")
w = {}
for p in range(4):
    vals, dvals, cvals = [], [], []
    for vs in reps[p][: (1 if p==0 else 200)]:
        D = dual_of(vs)
        dv = vol(D, 4-p)
        cv = 1.0 if p == 0 else simp_vol(vs, p)
        vals.append(dv/cv); dvals.append(dv); cvals.append(cv)
    vals = np.array(vals)
    w[p] = vals.mean()
    print("  p=%d : %3d cells, |cell| = %.6f (spread %.1e), |dual| = %.6f "
          "(spread %.1e)  ->  w = %.6f"
          % (p, len(vals), np.mean(cvals), np.ptp(cvals), np.mean(dvals),
             np.ptp(dvals), w[p]))
# p=4: dual is a point
vol16 = 2.0/3.0
w[4] = 1.0/vol16
print("  p=4 : |cell| = %.6f (16-cell), |dual| = 1  ->  w = %.6f" % (vol16, w[4]))
print()
print("ratios r_p = sqrt(w_{p+1}/w_p):")
r = [np.sqrt(w[p+1]/w[p]) for p in range(4)]
for p in range(4): print("   r_%d = %.6f" % (p, r[p]))
v_naive = [np.sqrt(6), 2/np.sqrt(6), 1/np.sqrt(6), np.sqrt(2)]
print()
print("velocities:  naive  ->  Hodge-corrected")
for p in range(4):
    print("   pair (%d,%d):  %.6f  ->  %.6f" % (p, p+1, v_naive[p], r[p]*v_naive[p]))

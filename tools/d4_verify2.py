"""Definitive checks: Aut(D_4), orbits, triangles, slices, improvement."""
import itertools, numpy as np, sympy as sp
from collections import Counter

p1,p2,p3,p4 = sp.symbols('p1 p2 p3 p4', real=True)
P = [p1,p2,p3,p4]; psq = sum(x**2 for x in P)

shell = lambda n2, R=5: [v for v in itertools.product(range(-R,R+1), repeat=4)
                         if sum(v) % 2 == 0 and sum(x*x for x in v) == n2]
S1 = np.array(shell(2)); S2 = np.array(shell(4)); S3 = np.array(shell(6))
print("shell sizes:", len(S1), len(S2), len(S3))

# ---- Aut(D_4) by brute force: isometries permuting the nearest-neighbour shell
basis = np.array([[1,-1,0,0],[0,1,-1,0],[0,0,1,-1],[0,0,1,1]])
G0 = basis @ basis.T
S1set = {tuple(v) for v in S1}
auts = []
for combo in itertools.product(range(24), repeat=2):          # prune on first two
    v0, v1 = S1[combo[0]], S1[combo[1]]
    if v0@v0 != G0[0,0] or v1@v1 != G0[1,1] or v0@v1 != G0[0,1]: continue
    for i2 in range(24):
        v2 = S1[i2]
        if v2@v0 != G0[2,0] or v2@v1 != G0[2,1] or v2@v2 != G0[2,2]: continue
        for i3 in range(24):
            v3 = S1[i3]
            if v3@v0 != G0[3,0] or v3@v1 != G0[3,1] or v3@v2 != G0[3,2] \
               or v3@v3 != G0[3,3]: continue
            imgs = np.array([v0,v1,v2,v3])
            M = np.linalg.solve(basis, imgs).T           # M b_i = v_i
            if not np.allclose(M, np.round(M)): continue
            M = np.round(M).astype(int)
            if {tuple(v) for v in (S1 @ M.T)} == S1set:
                auts.append(M)
print("|Aut(D_4)| =", len(auts), "   (W(F_4) has order 1152)")

A = [np.array(m) for m in auts]
def orbits(shell_pts):
    pts = {tuple(v) for v in shell_pts}; seen = set(); out = []
    for v in shell_pts:
        t = tuple(v)
        if t in seen: continue
        orb = {tuple(m @ v) for m in A}
        seen |= orb; out.append(sorted(orb)[0])
    return out
print("shell2 orbits (reps):", orbits(S2), " -> single orbit?" , len(orbits(S2))==1)
print("  shell2 composition:", Counter(tuple(sorted(map(abs,v))) for v in S2))

# are (2,0,0,0) and (1,1,1,1) related?  (the triality degeneracy)
tri = [m for m in A if tuple(m @ np.array([2,0,0,0])) == (1,1,1,1)]
print("(2,0,0,0) -> (1,1,1,1) by an automorphism:", len(tri) > 0)

# the pair used for the scaling fit must be genuinely inequivalent
S18 = np.array(shell(18, R=6))
o18 = orbits(S18)
def orb_of(v):
    return sorted({tuple(m @ np.array(v)) for m in A})[0]
print("|x|^2=18 : #orbits =", len(o18),
      "| (3,3,0,0) and (4,1,1,0) inequivalent:",
      orb_of([3,3,0,0]) != orb_of([4,1,1,0]))

# ---- degree-d invariant dimensions under the true Aut(D_4) -----------------
def inv_dim(deg):
    rows = []
    for mon in itertools.combinations_with_replacement(range(4), deg):
        acc = sp.Integer(0)
        for m in A:
            sub = [sum(int(m[j,i])*P[j] for j in range(4)) for i in range(4)]
            acc += sp.prod([sub[i] for i in mon])
        acc = sp.expand(acc)
        if acc != 0: rows.append(sp.Poly(acc, *P).as_dict())
    keys = sorted({k for r in rows for k in r})
    return sp.Matrix([[r.get(k,0) for k in keys] for r in rows]).rank()
for d in (2,4,6,8):
    print(f"  dim invariants of degree {d}:", inv_dim(d))

# ---- non-bipartiteness: triangles ------------------------------------------
tris = sum(1 for e,f in itertools.combinations(S1,2)
           if tuple(e-f) in S1set)
print("\ntriangles through a site (D_4):", tris,
      "| hypercubic: 0 (bipartite)")

# ---- time-slice / transfer-matrix structure --------------------------------
spatial = [v for v in S1 if v[3] == 0]; temporal = [v for v in S1 if v[3] != 0]
print("bonds within a slice:", len(spatial), "| bonds to t+-1:", len(temporal))
print("straight temporal bond (0,0,0,1) in D_4:", (0,0,0,1) in S1set)
print("site reflection t->-t preserves D_4:",
      all(((v[0],v[1],v[2],-v[3])) and (sum(v[:3])-v[3]) % 2 == 0 for v in S1))
print("link reflection t->1-t preserves D_4:",
      all((sum(v[:3]) + (1-v[3])) % 2 == 0 for v in S1))

# p_4 dependence of the kernel: coefficient structure
a = sp.symbols('a', positive=True)
K = sum(2*(1-sp.cos(sum(int(e[i])*P[i] for i in range(4)))) for e in S1)
K = sp.expand(sp.simplify(sp.expand_trig(sp.expand(K))))
Kc = sp.simplify(sp.collect(sp.expand(sp.simplify(K)), sp.cos(p4)))
print("\ncoefficient of cos(p4) in the D_4 kernel:",
      sp.simplify(sp.expand(K).coeff(sp.cos(p4))))

# ---- Symanzik improvement parameter counting -------------------------------
def moments(sh):
    m2 = sp.expand(sum((sum(int(e[i])*P[i] for i in range(4)))**2 for e in sh))
    m4 = sp.expand(sum((sum(int(e[i])*P[i] for i in range(4)))**4 for e in sh))
    return sp.simplify(m2/psq), sp.simplify(m4/psq**2)
for nm, sh in (("shell1", S1), ("shell2", S2), ("shell3", S3)):
    r2, r4 = moments(sh)
    print(f"{nm}: sum(p.e)^2 = {r2} p^2 ; sum(p.e)^4 / (p^2)^2 =",
          sp.simplify(r4), "(isotropic)" if sp.simplify(r4).is_number else "(ANISOTROPIC)")
c1, c2 = sp.symbols('c1 c2')
# K = c1*S1 + c2*S2 ; require p^2 coefficient = 1 and (p^2)^2 term = 0
A2 = sp.Rational(12), sp.Rational(24)      # sum (p.e)^2 = A2 * p^2  (filled below)
m2_1,_ = moments(S1); m2_2,_ = moments(S2)
m4_1 = sp.simplify(sum((sum(int(e[i])*P[i] for i in range(4)))**4 for e in S1)/psq**2)
m4_2 = sp.simplify(sum((sum(int(e[i])*P[i] for i in range(4)))**4 for e in S2)/psq**2)
sol = sp.solve([c1*m2_1 + c2*m2_2 - 1,
                c1*m4_1 + c2*m4_2], [c1,c2], dict=True)
print("improved D_4 couplings (normalise p^2, cancel (p^2)^2):", sol)

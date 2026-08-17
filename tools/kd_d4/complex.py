"""Translation-invariant cell complexes on D_4 and Z^4, with Bloch boundary
operators, ready for spectral analysis of the Kaehler-Dirac operator
K = d - d^dagger  (d = coboundary).

D_4: Delaunay complex = 16-cell honeycomb.  Cells per site [1,12,32,24,3].
Z^4: the usual cubical complex.             Cells per site [1,4,6,4,1].
"""
import itertools, numpy as np
from collections import defaultdict
from fractions import Fraction

# ============================================================== helpers
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))

def sort_sign(seq):
    """sort a sequence, returning (sorted tuple, parity of the permutation)"""
    idx = sorted(range(len(seq)), key=lambda i: seq[i])
    s = 1
    for i in range(len(idx)):
        for j in range(i + 1, len(idx)):
            if idx[i] > idx[j]: s = -s
    return tuple(seq[i] for i in idx), s


class Complex:
    """cells[p] : list of canonical orbit representatives
       bnd[p]   : dict (beta, alpha) -> {shift: coeff}   for  d_p : C_p -> C_{p-1}
       (alpha indexes a p-cell orbit, beta a (p-1)-cell orbit)"""

    def __init__(self, cells, boundary):
        self.cells = cells                     # {p: [rep,...]}
        self.index = {p: {c: i for i, c in enumerate(cs)} for p, cs in cells.items()}
        self.n = {p: len(cs) for p, cs in cells.items()}
        self.bnd = boundary                    # {p: {(beta,alpha): {shift: c}}}
        self.pmax = max(cells)

    def bloch_boundary(self, p, k):
        """matrix of  partial_p : C_p -> C_{p-1}  at momentum k"""
        M = np.zeros((self.n[p - 1], self.n[p]), complex)
        for (b, a), terms in self.bnd[p].items():
            M[b, a] = sum(c * np.exp(-1j * dot(k, d)) for d, c in terms.items())
        return M

    def bloch_d(self, k):
        """the full nilpotent coboundary d on  oplus_p C^p,  at momentum k.
        d_p = (partial_{p+1})^dagger in the orthonormal cochain basis."""
        offs, tot = {}, 0
        for p in range(self.pmax + 1):
            offs[p] = tot; tot += self.n[p]
        D = np.zeros((tot, tot), complex)
        for p in range(1, self.pmax + 1):
            B = self.bloch_boundary(p, k)          # (n_{p-1}, n_p)
            # d: C^{p-1} -> C^p  is B^dagger
            D[offs[p]:offs[p] + self.n[p], offs[p - 1]:offs[p - 1] + self.n[p - 1]] \
                = B.conj().T
        return D, offs, tot

    def K(self, k):
        D, offs, tot = self.bloch_d(k)
        return D - D.conj().T


# ============================================================== D_4
def build_D4():
    MIN = [v for v in itertools.product((-1, 0, 1), repeat=4)
           if sum(v) % 2 == 0 and sum(x * x for x in v) == 2]
    D4 = set(v for v in itertools.product(range(-4, 5), repeat=4) if sum(v) % 2 == 0)

    # ---- simplices (p = 0..3) as vertex sets containing the origin
    def cliques(k):
        return [c for c in itertools.combinations(MIN, k)
                if all(dot(c[i], c[j]) == 1
                       for i in range(k) for j in range(i + 1, k))]

    raw = {0: [((0, 0, 0, 0),)]}
    for p in (1, 2, 3):
        raw[p] = [tuple([(0, 0, 0, 0)] + list(c)) for c in cliques(p)]

    def canon_simplex(vs):
        """-> (canonical rep, shift, sign)  with rep's first vertex at origin"""
        s, sg = sort_sign(vs)
        t = s[0]
        return tuple(sub(v, t) for v in s), t, sg

    cells = {}
    for p in range(4):
        seen = {}
        for vs in raw[p]:
            rep, t, sg = canon_simplex(vs)
            seen[rep] = True
        cells[p] = sorted(seen)

    # ---- 4-cells: 16-cells centred on the 24 deep holes adjacent to 0
    holes = [tuple(Fraction(s if i == m else 0) for i in range(4))
             for m in range(4) for s in (1, -1)]
    holes += [tuple(Fraction(x, 2) for x in s)
              for s in itertools.product((1, -1), repeat=4)]

    def verts_of(h):
        return [v for v in D4
                if sum((Fraction(a) - b) ** 2 for a, b in zip(v, h)) == 1]

    def canon16(h):
        vs = verts_of(h)
        assert len(vs) == 8
        t = min(vs)
        h2 = tuple(a - b for a, b in zip(h, t))
        us, used = [], set()
        for v in sorted(vs, reverse=True):
            if v in used: continue
            u = tuple(Fraction(a) - b for a, b in zip(v, h))
            w = tuple(int(b - a) for a, b in zip(u, h))
            used.add(v); used.add(w); us.append(u)
        us.sort(reverse=True)          # canonical order of the four axes
        return (h2, tuple(us)), t

    seen = {}
    for h in holes:
        rep, t = canon16(h)
        seen[rep] = True
    cells[4] = sorted(seen, key=str)

    idx = {p: {c: i for i, c in enumerate(cs)} for p, cs in cells.items()}

    # ---- boundary maps
    bnd = {p: defaultdict(lambda: defaultdict(int)) for p in range(1, 5)}
    for p in range(1, 4):
        for a, rep in enumerate(cells[p]):
            for i in range(p + 1):
                face = rep[:i] + rep[i + 1:]
                frep, t, sg = canon_simplex(face)
                b = idx[p - 1][frep]
                bnd[p][(b, a)][t] += ((-1) ** i) * sg
    # 16-cell -> its 16 tetrahedra:  sum_s (prod s) [h+s_1 u_1, ..., h+s_4 u_4]
    for a, (h, us) in enumerate(cells[4]):
        for s in itertools.product((1, -1), repeat=4):
            tet = tuple(tuple(int(hh + ss * uu) for hh, uu in zip(h, u))
                        for ss, u in zip(s, us))
            frep, t, sg = canon_simplex(tet)
            b = idx[3][frep]
            bnd[4][(b, a)][t] += (s[0] * s[1] * s[2] * s[3]) * sg
    for p in bnd:
        for key in list(bnd[p]):
            bnd[p][key] = {d: c for d, c in bnd[p][key].items() if c}
            if not bnd[p][key]: del bnd[p][key]
        bnd[p] = dict(bnd[p])
    return Complex(cells, bnd)


# ============================================================== Z^4 (cubical)
def build_Z4():
    cells = {p: [H for H in itertools.combinations(range(4), p)] for p in range(5)}
    idx = {p: {c: i for i, c in enumerate(cs)} for p, cs in cells.items()}
    bnd = {p: defaultdict(lambda: defaultdict(int)) for p in range(1, 5)}
    for p in range(1, 5):
        for a, H in enumerate(cells[p]):
            for i, mu in enumerate(H):
                F = H[:i] + H[i + 1:]
                b = idx[p - 1][F]
                sgn = (-1) ** i
                sh = tuple(1 if j == mu else 0 for j in range(4))
                bnd[p][(b, a)][sh] += sgn        # (x+mu, F)
                bnd[p][(b, a)][(0, 0, 0, 0)] += -sgn
    for p in bnd:
        for key in list(bnd[p]):
            bnd[p][key] = {d: c for d, c in bnd[p][key].items() if c}
            if not bnd[p][key]: del bnd[p][key]
        bnd[p] = dict(bnd[p])
    return Complex(cells, bnd)


if __name__ == "__main__":
    for name, C in (("D_4", build_D4()), ("Z^4", build_Z4())):
        cv = [C.n[p] for p in range(5)]
        print(f"{name}: cells per site {cv}  total {sum(cv)}  "
              f"Euler {sum((-1)**p*c for p,c in enumerate(cv))}")
        rng = np.random.default_rng(1)
        worst = 0
        for _ in range(6):
            k = rng.normal(size=4)
            for p in range(2, 5):
                A = C.bloch_boundary(p - 1, k) @ C.bloch_boundary(p, k)
                worst = max(worst, np.abs(A).max())
            D, _, _ = C.bloch_d(k)
            worst = max(worst, np.abs(D @ D).max())
        print(f"    max |partial^2| and |d^2| over random k: {worst:.2e}")

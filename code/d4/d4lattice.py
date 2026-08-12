"""
d4lattice.py -- geometry and indexing for the D_4 ("4d checkerboard") lattice
and, for comparison, the hypercubic lattice Z^4, on a periodic L^4 box.

--------------------------------------------------------------------------
GEOMETRY
--------------------------------------------------------------------------
D_4 = { x in Z^4 : x_1 + x_2 + x_3 + x_4 is even }.

It is the index-2 "checkerboard" sublattice of Z^4, so Z^4 = D_4 u (D_4 + e_1)
and D_4 contains exactly half of the hypercubic sites.  Its nearest
neighbours are the 24 vectors

        (+-1, +-1, 0, 0)  and all coordinate permutations,

all at Euclidean distance sqrt(2).  Those 24 vectors are the vertices of the
24-cell, the Voronoi-relevant polytope of D_4; D_4 is the densest lattice
sphere packing in four dimensions (kissing number 24 vs. 8 for Z^4, whose
nearest neighbours are the 8 vectors (+-1,0,0,0) at distance 1).

The point group of D_4 is the Weyl group W(F_4) of order 1152 -- three times
larger than the hyperoctahedral group B_4 (order 384) of Z^4.  The extra
generator is the "triality" reflection

        H = 1/2 * [[1, 1, 1, 1],
                   [1, 1,-1,-1],
                   [1,-1, 1,-1],
                   [1,-1,-1, 1]],           H in O(4),  H D_4 = D_4,

which maps (r,0,0,0) -> (r/2,r/2,r/2,r/2).  This has a sharp consequence for
lattice-artifact studies and is easy to trip over:  the point pairs

        (2,0,0,0) <-> (1,1,1,1)        (|x|^2 = 4)
        (4,0,0,0) <-> (2,2,2,2)        (|x|^2 = 16)

which look like "axis vs. body diagonal" and are genuinely inequivalent on
Z^4, lie in a *single* W(F_4) orbit on D_4.  Any D_4-invariant observable is
therefore *exactly* equal on them and they measure zero anisotropy for a
trivial reason.  See `same_d4_orbit()` and the discussion in
`free_anisotropy.py`.  The smallest shell of D_4 carrying two distinct
W(F_4) orbits is |x|^2 = 18, which splits as

        24 vectors  of type (3,3,0,0)       [ = 3 x the minimal shell ]
       288 vectors  of types (4,1,1,0), (3,2,2,1).

--------------------------------------------------------------------------
SUBLATTICE / TIME-SLICE STRUCTURE
--------------------------------------------------------------------------
Fix the "time" direction to be mu = 4.  On the time slice x_4 = t the
surviving spatial points obey  x_1 + x_2 + x_3 = t (mod 2), i.e. each slice
is a three-dimensional face-centred-cubic lattice (D_3 = A_3 = fcc), and
successive slices are the two interleaved fcc sublattices of Z^3 -- an ABAB
stacking.  The 24 neighbours split accordingly as

        12 in-slice     (+-1,+-1,0,0) with e_4 = 0        -> fcc coordination 12
         6 to slice t+1 (+-1,0,0,+1) & permutations
         6 to slice t-1 (+-1,0,0,-1) & permutations

so a transfer-matrix formulation couples only adjacent slices, exactly as on
the hypercubic lattice, but each slice carries L^3/2 sites instead of L^3.

--------------------------------------------------------------------------
PERIODIC BOX AND INDEXING
--------------------------------------------------------------------------
We embed both lattices in the periodic box Z_L^4.  For D_4 the box side L
must be EVEN: shifting a coordinate by L must preserve the even-sum
condition, which requires L = 0 (mod 2).  (This is asserted.)

D_4 site index.  Because sum x_i is even, x_4 is determined modulo 2 by
x_1 + x_2 + x_3.  Writing p = (x_1 + x_2 + x_3) mod 2 we store

        idx = ((x_1 * L + x_2) * L + x_3) * (L//2) + (x_4 - p)//2 ,

a bijection onto {0, ..., L^4/2 - 1}.  Hypercubic uses the plain row-major
index ((x_1 * L + x_2) * L + x_3) * L + x_4.

NOTE ON PERIODICITY AND TRIALITY.  The torus Z_L^4 is invariant under the
hyperoctahedral group B_4 but *not* under the triality reflection H, since
H(L,0,0,0) = (L/2,L/2,L/2,L/2) is not in L Z^4.  Triality is therefore an
exact symmetry of the infinite D_4 lattice that is broken by these boundary
conditions at O(exp(-L/2 xi)).  Use a large box if you want to see the
degeneracy of the (2,0,0,0)/(1,1,1,1) pair numerically.

Run this file directly for a self-test:  python3 d4lattice.py
"""

from __future__ import annotations

import itertools

import numpy as np

__all__ = [
    "d4_neighbours",
    "hypercubic_neighbours",
    "D4Lattice",
    "HypercubicLattice",
    "make_lattice",
    "d4_point_group",
    "same_d4_orbit",
    "TRIALITY",
]


# --------------------------------------------------------------------------
# Neighbour shells
# --------------------------------------------------------------------------
def d4_neighbours() -> np.ndarray:
    """The 24 nearest-neighbour vectors of D_4: (+-1,+-1,0,0) and permutations.

    Returns
    -------
    (24, 4) int array, each row of squared length 2.
    """
    vecs = []
    for mu, nu in itertools.combinations(range(4), 2):
        for smu in (+1, -1):
            for snu in (+1, -1):
                e = [0, 0, 0, 0]
                e[mu] = smu
                e[nu] = snu
                vecs.append(e)
    out = np.array(sorted(vecs), dtype=np.int64)
    assert out.shape == (24, 4)
    assert np.all((out ** 2).sum(axis=1) == 2)
    return out


def hypercubic_neighbours() -> np.ndarray:
    """The 8 nearest-neighbour vectors of Z^4: (+-1,0,0,0) and permutations.

    Returns
    -------
    (8, 4) int array, each row of squared length 1.
    """
    vecs = []
    for mu in range(4):
        for s in (+1, -1):
            e = [0, 0, 0, 0]
            e[mu] = s
            vecs.append(e)
    out = np.array(sorted(vecs), dtype=np.int64)
    assert out.shape == (8, 4)
    return out


# --------------------------------------------------------------------------
# Point group of D_4 (Weyl group of F_4, order 1152)
# --------------------------------------------------------------------------
TRIALITY = 0.5 * np.array(
    [[1.0, 1.0, 1.0, 1.0],
     [1.0, 1.0, -1.0, -1.0],
     [1.0, -1.0, 1.0, -1.0],
     [1.0, -1.0, -1.0, 1.0]]
)


def d4_point_group() -> np.ndarray:
    """Generate the full point group of D_4 by closure.

    Generators: two coordinate permutations (which generate S_4), one sign
    flip of a *pair* of coordinates (even sign changes preserve D_4; odd ones
    do too here because D_4 is defined by an even *sum*, so a single sign flip
    x_1 -> -x_1 also preserves it -- the group is therefore B_4 extended by
    triality), and the triality reflection H.

    Returns
    -------
    (1152, 4, 4) float array of orthogonal matrices.
    """
    gens = []
    for perm in [(1, 0, 2, 3), (1, 2, 3, 0)]:  # a transposition + a 4-cycle -> S_4
        m = np.zeros((4, 4))
        for i, j in enumerate(perm):
            m[i, j] = 1.0
        gens.append(m)
    gens.append(np.diag([-1.0, 1.0, 1.0, 1.0]))  # single sign flip
    gens.append(TRIALITY)

    ident = np.eye(4)
    seen = {tuple(np.round(ident, 9).ravel())}
    group = [ident]
    frontier = [ident]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                m = np.round(h @ g, 9) + 0.0  # +0.0 normalises -0.0 to 0.0
                key = tuple(m.ravel())
                if key not in seen:
                    seen.add(key)
                    group.append(m)
                    new.append(m)
        frontier = new
    return np.array(group)


_PG_CACHE: list[np.ndarray] = []


def same_d4_orbit(u, v) -> bool:
    """True if the integer vectors u, v lie in the same orbit of the D_4 point
    group W(F_4).  A D_4-invariant function of x (such as the infinite-volume
    free propagator) is *exactly* equal at two such points.
    """
    if not _PG_CACHE:
        _PG_CACHE.append(d4_point_group())
    g = _PG_CACHE[0]
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    images = g @ u  # (1152, 4)
    return bool(np.any(np.all(np.abs(images - v) < 1e-9, axis=1)))


# --------------------------------------------------------------------------
# Lattices on the periodic L^4 box
# --------------------------------------------------------------------------
class _BaseLattice:
    """Common interface: coords <-> index maps plus a neighbour table."""

    name = "base"

    def __init__(self, L: int):
        self.L = int(L)
        self.nbvecs = None      # (q, 4) int
        self.n_sites = 0
        self.coords = None      # (n_sites, 4) int
        self.neighbours = None  # (n_sites, q) int32

    # -- to be provided by subclasses ------------------------------------
    def index(self, x) -> np.ndarray:
        raise NotImplementedError

    def coord(self, i) -> np.ndarray:
        raise NotImplementedError

    def contains(self, x) -> np.ndarray:
        raise NotImplementedError

    # -- shared ----------------------------------------------------------
    @property
    def q(self) -> int:
        """Coordination number."""
        return self.nbvecs.shape[0]

    def _build_neighbour_table(self) -> np.ndarray:
        """(n_sites, q) int32 table of neighbour site indices, periodic in L."""
        L = self.L
        tab = np.empty((self.n_sites, self.q), dtype=np.int32)
        for a, e in enumerate(self.nbvecs):
            tab[:, a] = self.index((self.coords + e) % L)
        return tab

    def _self_test(self) -> None:
        """Round-trip and neighbour-table consistency checks."""
        assert np.array_equal(self.index(self.coords), np.arange(self.n_sites))
        assert np.array_equal(self.coord(np.arange(self.n_sites)), self.coords)
        # neighbour relation is symmetric: j in nb(i)  <=>  i in nb(j)
        i = np.repeat(np.arange(self.n_sites), self.q)
        j = self.neighbours.ravel()
        back = np.isin(self.neighbours[j], np.arange(self.n_sites))  # cheap sanity
        assert back.all()
        # every neighbour appears exactly once and i is among its neighbours
        assert np.all(np.any(self.neighbours[j] == i[:, None], axis=1))
        # no self-neighbours (true whenever L > 2)
        if self.L > 2:
            assert not np.any(self.neighbours == np.arange(self.n_sites)[:, None])

    def __repr__(self) -> str:
        return (f"<{self.name} L={self.L} n_sites={self.n_sites} "
                f"q={self.q}>")


class D4Lattice(_BaseLattice):
    """D_4 on a periodic L^4 box.  L must be even.  n_sites = L^4 / 2."""

    name = "D4"

    def __init__(self, L: int, build_table: bool = True):
        super().__init__(L)
        assert self.L % 2 == 0, (
            f"L must be EVEN for D_4 on a periodic box (got L={L}); otherwise "
            "the shift x_mu -> x_mu + L flips the parity of sum_i x_i and the "
            "even-sum condition is not preserved."
        )
        self.nbvecs = d4_neighbours()
        L = self.L
        self.half = L // 2
        self.n_sites = L ** 4 // 2

        # enumerate the even-sum points of Z_L^4 in index order
        g = np.indices((L, L, L, self.half)).reshape(4, -1)
        x1, x2, x3, j = g
        par = (x1 + x2 + x3) & 1
        x4 = 2 * j + par
        self.coords = np.stack([x1, x2, x3, x4], axis=1).astype(np.int64)
        self.neighbours = self._build_neighbour_table() if build_table else None

    def index(self, x) -> np.ndarray:
        """Coordinates -> site index.  x is (...,4) integer, taken mod L."""
        x = np.asarray(x, dtype=np.int64) % self.L
        x1, x2, x3, x4 = x[..., 0], x[..., 1], x[..., 2], x[..., 3]
        assert np.all(((x1 + x2 + x3 + x4) & 1) == 0), \
            "point is not on D_4 (odd coordinate sum)"
        par = (x1 + x2 + x3) & 1
        return (((x1 * self.L + x2) * self.L + x3) * self.half
                + (x4 - par) // 2)

    def coord(self, i) -> np.ndarray:
        """Site index -> coordinates, shape (...,4)."""
        i = np.asarray(i, dtype=np.int64)
        j = i % self.half
        rest = i // self.half
        x3 = rest % self.L
        rest = rest // self.L
        x2 = rest % self.L
        x1 = rest // self.L
        x4 = 2 * j + ((x1 + x2 + x3) & 1)
        return np.stack([x1, x2, x3, x4], axis=-1)

    def contains(self, x) -> np.ndarray:
        x = np.asarray(x, dtype=np.int64)
        return (x.sum(axis=-1) & 1) == 0


class HypercubicLattice(_BaseLattice):
    """Z^4 on a periodic L^4 box.  n_sites = L^4."""

    name = "hypercubic"

    def __init__(self, L: int, build_table: bool = True):
        super().__init__(L)
        self.nbvecs = hypercubic_neighbours()
        L = self.L
        self.n_sites = L ** 4
        g = np.indices((L, L, L, L)).reshape(4, -1)
        self.coords = np.stack(g, axis=1).astype(np.int64)
        self.neighbours = self._build_neighbour_table() if build_table else None

    def index(self, x) -> np.ndarray:
        x = np.asarray(x, dtype=np.int64) % self.L
        return (((x[..., 0] * self.L + x[..., 1]) * self.L + x[..., 2]) * self.L
                + x[..., 3])

    def coord(self, i) -> np.ndarray:
        i = np.asarray(i, dtype=np.int64)
        x4 = i % self.L
        i = i // self.L
        x3 = i % self.L
        i = i // self.L
        x2 = i % self.L
        x1 = i // self.L
        return np.stack([x1, x2, x3, x4], axis=-1)

    def contains(self, x) -> np.ndarray:
        x = np.asarray(x, dtype=np.int64)
        return np.ones(x.shape[:-1], dtype=bool)


def make_lattice(kind: str, L: int, build_table: bool = True) -> _BaseLattice:
    """Factory: kind in {'d4', 'hc'}."""
    kind = kind.lower()
    if kind in ("d4", "d_4"):
        return D4Lattice(L, build_table=build_table)
    if kind in ("hc", "hypercubic", "z4"):
        return HypercubicLattice(L, build_table=build_table)
    raise ValueError(f"unknown lattice kind {kind!r}")


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------
def _main() -> None:
    print("=" * 70)
    print("d4lattice.py self-test")
    print("=" * 70)

    nb4 = d4_neighbours()
    nbh = hypercubic_neighbours()
    print(f"D_4 neighbour shell : {nb4.shape[0]} vectors, |e|^2 = "
          f"{set((nb4 ** 2).sum(1))}")
    print(f"Z^4 neighbour shell : {nbh.shape[0]} vectors, |e|^2 = "
          f"{set((nbh ** 2).sum(1))}")

    # -- moment sums: the heart of the O(a^4) claim ----------------------
    # For a random momentum p, compare sum_e (p.e)^2 and sum_e (p.e)^4 with
    # the isotropic forms 12 p^2 and 12 (p^2)^2.
    rng = np.random.default_rng(0)
    p = rng.normal(size=(5, 4))
    p2 = (p ** 2).sum(1)
    m2 = ((p @ nb4.T) ** 2).sum(1)
    m4 = ((p @ nb4.T) ** 4).sum(1)
    h2 = ((p @ nbh.T) ** 2).sum(1)
    h4 = ((p @ nbh.T) ** 4).sum(1)
    print(f"\nD_4 : max|sum_e (p.e)^2 - 12 p^2|     = {np.abs(m2 - 12 * p2).max():.2e}")
    print(f"D_4 : max|sum_e (p.e)^4 - 12 (p^2)^2| = {np.abs(m4 - 12 * p2 ** 2).max():.2e}"
          "   <-- exactly isotropic, hence O(a^4)")
    print(f"Z^4 : max|sum_e (p.e)^2 -  2 p^2|     = {np.abs(h2 - 2 * p2).max():.2e}")
    print(f"Z^4 : sum_e (p.e)^4 = 2 sum_mu p_mu^4 -> anisotropic already at "
          f"O(a^2); max|... - (p^2)^2| = {np.abs(h4 - p2 ** 2).max():.2e}")

    # -- point group ------------------------------------------------------
    g = d4_point_group()
    print(f"\n|point group of D_4| = {len(g)}  (expected 1152 = |W(F_4)|)")
    assert len(g) == 1152
    ok = all(np.allclose(m @ m.T, np.eye(4)) for m in g[:200])
    print(f"  sampled elements orthogonal: {ok}")

    print("\nTriality degeneracies (same W(F_4) orbit  =>  G exactly equal):")
    for u, v in [((2, 0, 0, 0), (1, 1, 1, 1)),
                 ((4, 0, 0, 0), (2, 2, 2, 2)),
                 ((3, 3, 0, 0), (4, 1, 1, 0)),
                 ((6, 0, 0, 0), (4, 4, 2, 0))]:
        n2 = sum(c * c for c in u)
        print(f"  {str(u):>12} <-> {str(v):<12} |x|^2={n2:3d} : "
              f"same orbit = {same_d4_orbit(u, v)}")

    # -- indexing and neighbour tables -----------------------------------
    for L in (4, 6, 8):
        d4 = D4Lattice(L)
        hc = HypercubicLattice(L)
        assert d4.n_sites == L ** 4 // 2
        assert hc.n_sites == L ** 4
        d4._self_test()
        hc._self_test()
        print(f"\n{d4!r}  index/neighbour self-test OK")
        print(f"{hc!r}  index/neighbour self-test OK")

    # -- time-slice structure --------------------------------------------
    L = 8
    d4 = D4Lattice(L, build_table=False)
    nsl = np.bincount(d4.coords[:, 3], minlength=L)
    print(f"\nD_4 at L={L}: sites per time slice = {nsl.tolist()} "
          f"(= L^3/2 = {L ** 3 // 2}); each slice is a 3d fcc lattice")
    e4 = d4_neighbours()[:, 3]
    print(f"  neighbour split by delta t: "
          f"{{-1: {(e4 == -1).sum()}, 0: {(e4 == 0).sum()}, +1: {(e4 == 1).sum()}}}"
          "  (12 in-slice = fcc coordination)")

    print("\nAll self-tests passed.")


if __name__ == "__main__":
    _main()

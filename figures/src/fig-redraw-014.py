"""Redraw of fig-notes-014: a maximal tree gauge.  The red links form a
spanning tree of the lattice (no closed loops); all of them are set to 1 by
gauge transformations, and any additional red link would create a cycle.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_GREEN = "#009E73"

NX, NY = 10, 6  # sites

# ---- build a spanning (maximal) tree with randomized Kruskal ---------------
edges = ([((x, y), (x + 1, y)) for x in range(NX - 1) for y in range(NY)]
         + [((x, y), (x, y + 1)) for x in range(NX) for y in range(NY - 1)])
rng = np.random.default_rng(12)
order = rng.permutation(len(edges))

parent = {(x, y): (x, y) for x in range(NX) for y in range(NY)}


def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


tree = []
for k in order:
    a, b = edges[k]
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb
        tree.append((a, b))
assert len(tree) == NX * NY - 1  # spanning tree: maximal, no cycles

fig, ax = plt.subplots(figsize=(4.9, 3.3))
ax.set_aspect("equal")
ax.axis("off")

# ---- underlying lattice (green) --------------------------------------------
for x in range(NX):
    ax.plot([x, x], [-0.45, NY - 1 + 0.45], color=C_GREEN, lw=1.1, zorder=1)
for y in range(NY):
    ax.plot([-0.45, NX - 1 + 0.45], [y, y], color=C_GREEN, lw=1.1, zorder=1)

# ---- tree links (red) ------------------------------------------------------
for (a, b) in tree:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_RED, lw=2.8,
            solid_capstyle="round", zorder=2)

# ---- annotation ------------------------------------------------------------
target = next(((a, b) for (a, b) in tree
               if a[1] == NY - 1 and b[1] == NY - 1 and 1 <= a[0] <= 4), None)
if target is None:  # fall back to any tree link touching the top row
    target = next((a, b) for (a, b) in tree if b[1] == NY - 1)
mid = (0.5 * (target[0][0] + target[1][0]), 0.5 * (target[0][1] + target[1][1]))
ax.annotate("links set to $1$", xy=mid, xytext=(mid[0] + 1.8, NY + 0.55),
            color=C_RED, fontsize=10, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.2,
                            shrinkB=3))

ax.set_xlim(-0.8, NX - 0.2)
ax.set_ylim(-0.8, NY + 0.9)

fig.savefig("../fig-redraw-014.pdf")
fig.savefig("../fig-redraw-014.png", dpi=200)
print("done 014")

import os
import sys

# Adding required CLRS directories to the Python path
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
clrs_dir = os.path.join(parent_dir, 'clrsPython')

for folder in ["Chapter 21", "Utility functions", "Chapter 6", "Chapter 10", "Chapter 2", "Chapter 19"]:
    sys.path.append(os.path.join(clrs_dir, folder))

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, prim, get_total_weight

# 1) Labels and an index map for the toy dataset
labels = ['A', 'B', 'C', 'D', 'E']
index = {v: i for i, v in enumerate(labels)}

# 2) Build undirected, weighted graph from the Task 2a toy data
# Edges: AB=4, AC=3, BC=1, BD=2, CE=5, DE=3
edges = [
    ('A', 'B', 4),
    ('A', 'C', 3),
    ('B', 'C', 1),
    ('B', 'D', 2),
    ('C', 'E', 5),
    ('D', 'E', 3),
]

G = AdjacencyListGraph(len(labels), False, True)
for u, v, w in edges:
    G.insert_edge(index[u], index[v], w)

# 3) Compute MST with Kruskal (you may also show Prim for parity)
mst_k = kruskal(G)
total_k = get_total_weight(mst_k)

mst_p = prim(G, index['A'])
total_p = get_total_weight(mst_p)

# 4) Extract MST edge set in label form
def undirected_edge_list(graph):
    out = []
    for u in range(graph.get_card_V()):
        for e in graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                out.append((labels[u], labels[v], e.get_weight()))
    # Sort nicely by weight then lexicographically
    out.sort(key=lambda t: (t[2], t[0], t[1]))
    return out

mst_edges = undirected_edge_list(mst_k)

# 5) Compute closable edges = original edges not in MST
mst_set = {(min(a, b), max(a, b)) for (a, b, _) in mst_edges}
closable = []
for (u, v, w) in edges:
    a, b = min(u, v), max(u, v)
    if (a, b) not in mst_set:
        closable.append((a, b, w))
closable.sort(key=lambda t: (t[2], t[0], t[1]))

# 6) Print results
print("Vertices:", labels)
print("All edges (toy):", sorted([(min(u, v), max(u, v), w) for (u, v, w) in edges], key=lambda t: (t[2], t[0], t[1])))
print("MST (Kruskal):", mst_edges)
print("MST total weight (Kruskal):", total_k)
print("MST total weight (Prim):", total_p)
print("Closable (non-MST) edges:", closable)
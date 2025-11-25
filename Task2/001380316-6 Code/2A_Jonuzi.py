import os
import sys
from time import perf_counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_directory_upwards(start_dir, target_name, max_levels=10):
    #search through the filesystem until it finds the clrs folder
    current = start_dir

    for _ in range(max_levels + 1):
        candidate = os.path.join(current, target_name)
        if os.path.isdir(candidate):
            return candidate

        parent = os.path.dirname(current)
        if parent == current:   # reached filesystem root
            print("CLRS folder not found")
            break
        current = parent

    raise FileNotFoundError(
        f"Could not find directory '{target_name}' within {max_levels} levels above {start_dir}"
    )

#look for the clrs folder above the folder the code is stored in
CLRS_DIR = find_directory_upwards(BASE_DIR, "clrsPython", max_levels=10)

for subfolder in ["Utility functions", "Chapter 20", "Chapter 22", "Chapter 10", "Chapter 6"]:
    sys.path.append(os.path.join(CLRS_DIR, subfolder))


from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

def build_test_graph():

    stations = ["A","B","C","D","E"]
    n = len(stations)

    graph = AdjacencyListGraph(card_V =n, directed = False, weighted = True)

    edges = [
        (0, 1, 4),   #A-B distance
        (0, 2, 2),   #A-C distance
        (1, 2, 1),   #B-C distance
        (1, 3, 5),   #B-D distance
        (2, 3, 8),   #C-D distance
        (2, 4, 10),  #C-E distance
        (3, 4, 2),   #D-E distance
    ]

    for u, v, w in edges:
        graph.insert_edge(u, v, weight = w)

    return graph, stations

def run_example():
    graph, stations = build_test_graph()

    start_name = "A"
    dest_name = "D"

    #Map station names to indices using a dictionary
    name_to_index = {name: idx for idx, name in enumerate(stations)}
    s = name_to_index[start_name]
    t = name_to_index[dest_name]

    #Call dijkstra function to compute shortest distance
    t0 = perf_counter()
    d, pi = dijkstra(graph, s)
    t1 = perf_counter()

    total_time = d[t]

    #Reconstruct the route as their original station names
    route = print_path(pi, s, t, lambda i: stations[i])

    print("Test Run with 5 Stations")
    print(f"Start station:       {start_name}")
    print(f"Destination station: {dest_name}")
    print(f"Shortest route:      {' -> '.join(route)}")
    print(f"Total journey time:  {total_time} minutes")
    print(f"Dijkstra runtime:    {(t1 - t0):.6f} seconds")

if __name__ == "__main__":
    run_example()
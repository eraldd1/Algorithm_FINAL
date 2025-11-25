import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
clrs_dir = os.path.join(parent_dir, 'clrsPython')
chapter21_dir = os.path.join(clrs_dir, 'Chapter 21')
utility_dir = os.path.join(clrs_dir, 'Utility functions')
chapter6_dir = os.path.join(clrs_dir, 'Chapter 6')
chapter10_dir = os.path.join(clrs_dir, 'Chapter 10')
chapter22_dir = os.path.join(clrs_dir, 'Chapter 22')
chapter24_dir = os.path.join(clrs_dir, 'Chapter 24')

for path in [chapter21_dir, utility_dir, chapter6_dir, chapter10_dir, chapter22_dir, chapter24_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import CLRS algorithms and structures
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

#defining the small tube network
stations = ['A', 'B', 'C', 'D', 'E']
station_to_index = {name: i for i, name in enumerate(stations)}

#clean list of edges with each inserted once
edges = [
    ('A', 'B', 4),
    ('A', 'C', 3),
    ('B', 'A', 4),
    ('B', 'C', 1),
    ('B', 'D', 2),
    ('C', 'A', 3),
    ('C', 'B', 1),
    ('C', 'E', 5),
    ('D', 'B', 2),
    ('D', 'E', 3),
    ('E', 'C', 5),
    ('E', 'D', 3),
]


#building the graph using the needed CLRS class
graph = AdjacencyListGraph(len(stations), directed=True, weighted=True)
for u_name, v_name, weight in edges:
    u = station_to_index[u_name]
    v = station_to_index[v_name]
    graph.insert_edge(u, v, weight)


#input functions
def prompt_station(prompt_message):
    while True:
        try:
            response = input(prompt_message).strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Exiting program.")
            sys.exit(1)

        if response in station_to_index:
            return response

        print(f"Invalid station. Choose from: {', '.join(stations)}")


#running Dijkstra using clrs and making a minimal user interface

print("\nAvailable stations:", ", ".join(stations))

source = prompt_station("\nEnter the station where you start: ")
destination = prompt_station("Enter the destination station: ")

source_idx = station_to_index[source]
destination_idx = station_to_index[destination]

distances, predecessors = dijkstra(graph, source_idx)


#reconstructing paths

def reconstruct_path(pre_list, start_idx, end_idx):
    path = []
    current = end_idx

    while current is not None and current != -1:
        path.insert(0, current)
        current = pre_list[current]

    if not path or path[0] != start_idx:
        return None

    return [stations[i] for i in path]

shortest_path = reconstruct_path(predecessors, source_idx, destination_idx)


#output for all info between stations
if shortest_path is None or distances[destination_idx] == float('inf'):
    print(f"\nNo path exists from {source} to {destination}.")
else:
    print(f"\nShortest path from {source} to {destination}: {' -> '.join(shortest_path)}")
    print(f"Total journey duration: {distances[destination_idx]} minutes")
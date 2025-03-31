"""The plan:
1. Remove all vertices that aren't connected to a computer starting with "T"
4. Profit"""
from copy import copy
from line_profiler import profile
import sys
import resource

def parse_data():
    """Returns a dict representing a graph
    Key: vertex
    item: list of vertices connected to the key vertex"""
    with open("input-data/day23.txt") as file:
        lines = file.read().splitlines()
    graph = {f"{chr(x)}"+f"{chr(y)}":[]
             for x in range(ord('a'),ord('z')+1)
             for y in range(ord('a'),ord('z')+1)}
    for line in lines:
        a,b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)
    graph = {k: v for k, v in graph.items() if v != []}
    return graph

def remove_vertex(graph: dict[str, list[str]], removed_vertex: str):
    for v in graph:
        try:
            graph[v].remove(removed_vertex)
        except:
            continue
    del graph[removed_vertex]

def part_one():
    """Finds all cliques K3, filters down to cliques containing a computer starting with 't'"""
    graph = parse_data()
    sorted_vertices = sorted(graph.keys(), key=lambda x: len(graph[x]))
    triangles = []
    for v in sorted_vertices:
        marked = copy(graph[v])
        for u in graph[v]:
            for w in graph[u]:
                if w in marked:
                    triangles.append((v,u,w))
            marked.remove(u)
        remove_vertex(graph, v)
    t_tris = [x for x in triangles if any(y[0] == "t" for y in x)]
    answer = len(t_tris)
    print(answer)

def part_two():
    """Finds the maximum clique"""
    graph = parse_data()
    graph = {k: set(v) for k, v in graph.items()}
    sorted_graph = sorted(graph.keys(), key=lambda x: len(graph[x]))
    all_candidates = sorted_graph
    max_clique = []
    max_size = 0
    def find_largest_clique(candidates: list[str], size: int, current_clique: list[str]):
        nonlocal max_size, max_clique, graph
        if len(candidates) == 0:
            if size > max_size:
                max_size = size
                max_clique = current_clique
            return
        while candidates:
            if size+len(candidates) <= max_size:
                return
            i = candidates.pop(0)
            new_clique = copy(current_clique) + [i]
            new_candidates = [x for x in candidates if x in graph[i]]
            find_largest_clique(new_candidates, size+1, new_clique)
    find_largest_clique(all_candidates, 0, [])
    print(','.join(sorted(max_clique)))

part_one()
part_two()

"""Part one's algorithm was taken from:
Chiba, N.; Nishizeki, T. (1985), "Arboricity and subgraph listing algorithms", SIAM Journal on Computing, 14 (1): 210–223
available here:
https://www.cs.cornell.edu/courses/cs6241/2019sp/readings/Chiba-1985-arboricity.pdf

Part two's was taken from "A fast algorithm for the maximum clique problem", Patric R.J. Östergård,
DIscrete Applied Mathematics v.120 iss.1-3, 197-207
available here:
https://www.sciencedirect.com/science/article/pii/S0166218X01002906
"""
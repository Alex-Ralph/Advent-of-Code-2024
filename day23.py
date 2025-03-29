"""The plan:
1. Remove all vertices that aren't connected to a computer starting with "T"
4. Profit"""
from copy import copy
from line_profiler import profile
import sys
import resource

def parse_data():
    """Returns a dict representing a graph
    the graph is sorted by vertex weight from lightest to heaviest
    Key: vertex, values: connected vertices"""
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

def sort_graph(graph: dict[str, list[str]]) -> tuple[str]:
    """Returns tuple of graph items sorted by their weight, lowest to highest"""
    return sorted(graph.keys(), key=lambda x: len(graph[x]))

def part_one():
    """Finds all cliques K3, filters down to cliques containing a computer starting with 't'"""
    graph = parse_data()
    sorted_vertices = sort_graph(graph)
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

def expand(graph, candidates, clique):
    maximum_clique = clique
    for p in candidates:
        new_clique = clique + [p]
        new_candidates = candidates & graph[p]
        if candidates:
            new_clique = expand(graph, new_candidates, new_clique)
        if len(new_clique) > len(maximum_clique):
            maximum_clique = new_clique
    return maximum_clique

def part_two():
    """Finds the maximum clique"""
    resource.setrlimit(resource.RLIMIT_STACK, [0x1000000, resource.RLIM_INFINITY])
    sys.setrecursionlimit(0x10000)
    graph = parse_data()
    graph = {k: set(v) for k, v in graph.items()}
    sorted_graph = sort_graph(graph)
    max_degree = len(graph[sorted_graph[-1]])
    candidates = set(sorted_graph)
    print(len(candidates))
    maximum_clique = expand(graph, candidates, [])
    sorted_clique = sorted(maximum_clique)
    print(','.join(sorted_clique))

part_one()
part_two()

"""Part one's algorithm was taken from:
Chiba, N.; Nishizeki, T. (1985), "Arboricity and subgraph listing algorithms", SIAM Journal on Computing, 14 (1): 210–223"""
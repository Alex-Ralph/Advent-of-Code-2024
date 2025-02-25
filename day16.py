from heapq import heappop, heappush
import curses

class Node:
    def __init__(self, coord, vertical):
        self.coord = coord
        self.vertical = vertical

    def __str__(self):
        return f"{self.coord}, {self.vertical}"

    def __gt__(self, other):
        return abs(self.coord) > abs(other.coord)

    def __lt_(self, other):
        return abs(self.coord) < abs(other.coord)

    def __eq__(self, other):
        return self.coord == other.coord and self.vertical == other.vertical

    def __hash__(self):
        return hash((self.coord, self.vertical))

def parse_data():
    maze_string = open("input-data/day16.txt").read()
    return {x + 1j * y: val for y, line in enumerate(maze_string.split("\n"))
       for x, val in enumerate(line)}

MOVE_COST = 1
TURN_COST = 1000

def find_paths(maze, start_point, end_point, start_direction, stdscr=None):
    visited = {Node(x, True): -1 for x in maze.keys()}
    visited.update({Node(x, False): -1 for x in maze.keys()})
    nodes = []
    first_node = Node(start_point, start_direction)
    heappush(nodes, (0, first_node))
    maze_width = int(max(maze.keys(), key=lambda x: x.real).real) + 1
    maze_height = int(max(maze.keys(), key=lambda x: x.imag).imag) + 1
    while nodes:
        cost, vertex = heappop(nodes)
        vertex.cost = cost
        visited[vertex] = cost
        if maze[vertex.coord] == "#":
            continue
        elif vertex.coord == end_point:
            nodes_visited = len([x for x in visited.items() if x[1]])
            return (cost, visited)
        other_axis = Node(vertex.coord, not vertex.vertical)
        if visited[other_axis] == -1:
            heappush(nodes, (cost+TURN_COST, other_axis))
        direction = 1j if vertex.vertical else 1
        for new_node in [Node(vertex.coord + direction, vertex.vertical), 
                         Node(vertex.coord - direction, vertex.vertical)]:
            if visited[new_node] == -1:
                heappush(nodes, (cost + MOVE_COST, new_node))

def main(stdscr=None):
    """Hacky assumption for part two: the shortest path must end by entering the final tile vertically
    This is not an optimal solution but it was the easiest way to modify my
    part one code to get an answer quickly"""
    maze = parse_data()
    start_point = next(x for x in maze.keys() if maze[x] == "S")
    end_point = next(x for x in maze.keys() if maze[x] == "E")
    path_length, nodes_from_start=find_paths(maze, start_point, end_point, False, stdscr)
    nodes_from_start = {x: y for x, y in nodes_from_start.items() if y > 0}
    _, nodes_from_end=find_paths(maze, end_point, start_point, True, stdscr)
    nodes_from_end = {x: y for x, y in nodes_from_end.items() if y > 0}
    path_tiles = []
    for node, cost_from_start in nodes_from_start.items():
        if node in nodes_from_end:
            if nodes_from_end[node] + cost_from_start == path_length:
                path_tiles.append(node.coord)
    path_tiles = list(set(path_tiles))
    path_tiles = [x for x in path_tiles if maze[x] != "#"]
    print(f"Part one: {path_length}")
    print(f"Part two: {len(path_tiles)+1}")

if __name__ == "__main__":
    main()
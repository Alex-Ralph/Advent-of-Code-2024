from heapq import heapify, heappop, heappush
import curses
"""
this might be faster if we only consider nodes with multiple possible directions to be nodes
May also be worth considering it a directed graph?
A* optimisations may also help
Maybe also just consider your code, maybe we can remove the Node class
Walls are added to visited, right? Maybe we can remove them from the list of nodes to speed things up
Could you DFS and then optimise it? This seems like the longest shot

Immediate plan: Only consider nodes where a decision might be made to be "nodes" and when you visit each, 
work out which ones it's connected to
A* with crow-flies distance to the end as the parameter for solving
"""


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

def print_position(maze, node, visited):
    current_line = ""
    maze_width = int(max(maze.keys(), key=lambda x: x.real).real) + 1
    maze_height = int(max(maze.keys(), key=lambda x: x.imag).imag) + 1
    out = ""
    for y in range(maze_height):
        for x in range(maze_width):
            coord = x+1j*y
            if coord == node.coord:
                out += "O"
            elif (maze[coord] == "." and
                (visited[Node(coord, True)] or visited[Node(coord, False)])):
                out += "X"
            else: out += maze[coord]
        out += "\n"
    print(out)

def part_one():
    maze = parse_data()
    start_point = next(x for x in maze.keys() if maze[x] == "S")
    visited = {Node(x, True): False for x in maze.keys()}
    visited.update({Node(x, False): False for x in maze.keys()})
    nodes = []
    heappush(nodes, (0, Node(start_point, False)))
    while nodes:
        cost, vertex = heappop(nodes)
        visited[vertex] = True
        if maze[vertex.coord] == "#":
            continue
        elif maze[vertex.coord] == "E":
            # print_position(maze, vertex, visited)
            print(f"Solution found, value: {cost}")
            print(f"Nodes visited: {len([x for x in visited.items() if x[1]])}/{len(visited.keys())}")
            break
        other_axis = Node(vertex.coord, not vertex.vertical)
        if visited[other_axis] == False:
            heappush(nodes, (cost+TURN_COST, other_axis))
        direction = 1j if vertex.vertical else 1
        for new_node in [Node(vertex.coord + direction, vertex.vertical), 
                         Node(vertex.coord - direction, vertex.vertical)]:
            if visited[new_node] == False:
                heappush(nodes, (cost + MOVE_COST, new_node))
part_one()
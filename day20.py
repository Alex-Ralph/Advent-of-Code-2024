from collections import deque
from copy import copy
INPUT_FILE="input-data/day20.txt"

def parse_data() -> dict[complex: str]:
    with open(INPUT_FILE) as file:
        data = file.read()
        maze = {x + y*1j: val for y, line in enumerate(data.split("\n"))
                for x, val in enumerate(line)}
    return maze

def solve_maze(maze: dict[complex: str], start: complex) -> dict[complex: int]:
    """Returns list of distances of all nodes from the starting coordinate
    performs a simple BFS"""
    node_costs = {x: float('inf') for x in maze.keys() if maze[x] != "#"}
    node_costs[start] = 0
    queue = deque([(start, 0)])
    while queue:
        coord, cost = queue.popleft()
        for new in [coord+1, coord-1, coord+1j, coord-1j]:
            if new not in node_costs:
                continue
            if node_costs[new] > cost+1:
                node_costs[new] = cost+1
                queue.append((new, cost+1))
    return node_costs

def coords_at_distance(coord: complex, distance: int) -> set[complex]:
    """Returns crow-flies coordinates of each point a given distance away from a coordinate"""
    destinations = []
    for x in range(-distance, distance+1):
        destinations.append(coord.real + x + 1j * (coord.imag + distance - abs(x)))
        destinations.append(coord.real + x + 1j * (coord.imag - distance + abs(x)))
    return set(destinations)

def remove_inf(costs: dict[complex: int]) -> dict[complex: int]:
    return {x: y for x, y in costs.items() if y != float('inf')}

def solve(glitch_time: int, minimum_time_saved: int) -> int:
    maze = parse_data()
    start = next(x for x in maze.keys() if maze[x] == "S")
    end = next(x for x in maze.keys() if maze[x] == "E")
    costs_from_start = remove_inf(solve_maze(maze, start))
    costs_from_end = remove_inf(solve_maze(maze, end))
    cost_no_cheat = costs_from_start[end]
    cheat_counter = 0
    for node, cost in costs_from_start.items():
        for distance in range(2, glitch_time+1):
            for coord in coords_at_distance(node, distance):
                if (coord in costs_from_end and
                cost + distance + costs_from_end[coord] <= cost_no_cheat - minimum_time_saved):
                    cheat_counter += 1
    return cheat_counter

print(f"Part one: {solve(2, 100)}")
print(f"Part two: {solve(20, 100)}")
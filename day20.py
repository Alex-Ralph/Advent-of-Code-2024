from collections import deque
from copy import copy
INPUT_FILE="input-data/day20.txt"

WIDTH=0
HEIGHT=0
def parse_data() -> dict[complex: str]:
    global WIDTH
    global HEIGHT
    with open(INPUT_FILE) as file:
        data = file.read()
        WIDTH = len(data.split("\n")[0])
        HEIGHT = len(data.split("\n"))
        maze = {x + y*1j: val for y, line in enumerate(data.split("\n"))
                for x, val in enumerate(line)}
    return maze

def solve_maze(maze: dict[complex: int], start: complex, end: complex=None):
    """If end is not set, returns all reachable nodes
    if end is set, returns the cost of reaching that node"""
    node_costs = copy(maze)
    queue = deque([(start, node_costs[start])])
    while queue:
        coord, cost = queue.popleft()
        for new in [coord+1, coord-1, coord+1j, coord-1j]:
            if new not in node_costs:
                continue
            if node_costs[new] > cost+1:
                node_costs[new] = cost+1
                queue.append((new, cost+1))
    if end:
        return node_costs[end]
    return node_costs

def find_reachable_walls(node_costs: dict[complex: int], original_maze: dict[complex: str]) -> dict[complex: int]:
    reachable_nodes = [(x, y) for x, y in node_costs.items() if y != float('inf')] # TODO this needs sorting to work properly
    reachable_nodes = sorted(reachable_nodes, key=lambda x: x[1], reverse=True)
    walls = {
        a: cost+1
        for node, cost in reachable_nodes
        for neighbour in [1, -1, 1j, -1j]
        if original_maze[a:=node+neighbour] == "#"
        and (0 < a.imag <= HEIGHT and 0 < a.real <= WIDTH)
    }
    return walls

def part_one():
    maze = parse_data()
    start = next(x for x in maze.keys() if maze[x] == "S")
    end = next(x for x in maze.keys() if maze[x] == "E")
    node_costs = {key: float('inf') for key, val in maze.items() if val != "#"}
    node_costs[start] = 0
    no_cheat_costs = solve_maze(node_costs, start)
    reachable_walls = find_reachable_walls(no_cheat_costs, maze)
    cheats = []
    base_time = no_cheat_costs[end]
    for wall, cost in reachable_walls.items():
        no_cheat_costs.update({wall: cost})
        cheats.append(solve_maze(no_cheat_costs, wall, end))
        no_cheat_costs.pop(wall)
    timesaves = [base_time-x for x in cheats if base_time-x >= 100]
    counts = {i: timesaves.count(i) for i in timesaves}
    print(sum(counts.values()))

def remove_inf(costs):
    return {x: y for x, y in costs.items() if y != float('inf')}

def coords_at_distance(coord: complex, distance: int):
    destinations = []
    for x in range(-distance, distance+1):
        destinations.append(coord.real + x + 1j * (coord.imag + distance - abs(x)))
        destinations.append(coord.real + x + 1j * (coord.imag - distance + abs(x)))
    return list(set(destinations))

def part_two():
    """Find distances from the start, and distances from the end
    for each relevant node (must think more on how to determine this)
    find all the nodes it can reach and connect them "as the crow flies"
    see if that saves enough time
    """
    glitch_time = 20
    minimum_time_saved = 100
    maze = parse_data()
    start = next(x for x in maze.keys() if maze[x] == "S")
    end = next(x for x in maze.keys() if maze[x] == "E")
    node_costs = {key: float('inf') for key, val in maze.items() if val != "#"}
    node_costs[start] = 0
    costs_from_start = solve_maze(node_costs, start)
    node_costs[start] = float('inf')
    node_costs[end] = 0
    costs_from_end = solve_maze(node_costs, end)
    costs_from_start = remove_inf(costs_from_start)
    costs_from_end = remove_inf(costs_from_end)
    cost_no_cheat = costs_from_start[end]
    cheat_counter = 0
    for node, cost in costs_from_start.items():
        for distance in range(1, glitch_time+1):
            for coord in coords_at_distance(node, distance):
                if (coord in costs_from_end and
                cost + distance + costs_from_end[coord] <= cost_no_cheat - minimum_time_saved):
                    cheat_counter += 1
    print(cheat_counter)

part_one()
part_two()
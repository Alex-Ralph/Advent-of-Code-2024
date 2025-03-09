INPUT_FILE="test-data/day20.txt"
from collections import deque
WIDTH = 0
HEIGHT = 0

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

def solve_maze(maze: dict[complex: bool], start: complex, end: complex) -> int:
    node_costs = {x+1j*y: float('inf') for x in range(WIDTH) for y in range(HEIGHT)}
    queue = deque([(start, 0)])
    while queue:
        coord, cost = queue.popleft()
        if not maze[coord]:
            continue
        for new in [coord+1, coord-1, coord+1j, coord-1j]:
            if not ((0 <= new.real < WIDTH) and (0 <= new.imag < HEIGHT)):
                continue
            if not maze[new]:
                continue
            if node_costs[new] > cost+1:
                node_costs[new] = cost+1
                queue.append((new, cost+1))
    return node_costs[end]

def part_one():
    maze = parse_data()
    start = next(x for x in maze.keys() if maze[x] == "S")
    end = next(x for x in maze.keys() if maze[x] == "E")
    optimised_maze = {key: (not val == "#") for key, val in maze.items()}
    # can currently solve a maze properly, have to work out how to remove walls and then solve
    # the new maze
    # ideally only solve the section of maze that would change

part_one()
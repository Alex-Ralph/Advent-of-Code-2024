from collections import deque
from copy import copy
# WIDTH=7
# HEIGHT=7
# INPUT_FILE = "../test-data/day18.txt"
# TIME=12
WIDTH=71
HEIGHT=71
INPUT_FILE="input-data/day18.txt"
TIME=1024
def parse_data():
    with open(INPUT_FILE) as input:
        lines = input.read().split("\n")
        return [int(x) + int(y) * 1j for line in lines for x, y in [line.split(",")]]

BYTE_LIST = parse_data()

def get_maze_at_time(time: int):
    return set(BYTE_LIST[0:time])

def solve_maze(maze: dict[complex: bool]):
    start = 0+0j
    end = WIDTH-1 + (HEIGHT-1)*1j
    queue = deque([(start, 0)])
    node_costs = {x+1j*y: float('inf') for x in range(WIDTH) for y in range(HEIGHT)}
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
    maze = {x + y*1j: True for x in range(WIDTH) for y in range(HEIGHT)}
    walls = get_maze_at_time(TIME)
    for wall in walls:
        maze[wall] = False
    print(solve_maze(maze))
    
def part_two():
    """Binary search to find the first maze that does not have a valid solution"""
    maze = {x + y*1j: True for x in range(WIDTH) for y in range(HEIGHT)}
    bytes = deque(BYTE_LIST, len(BYTE_LIST))
    mazes = {}
    i = 0
    mazes[0] = copy(maze)
    while bytes:
        i += 1
        maze[bytes.popleft()] = False
        mazes[i] = copy(maze)
    min=0
    max=len(BYTE_LIST)
    while (max - min != 1):
        avg = int((max + min)/2)
        if solve_maze(mazes[avg]) == float('inf'):
            max=avg
        else: min=avg
    print(BYTE_LIST[min])

# def part_two():
#     maze = {x + y*1j: True for x in range(WIDTH) for y in range(HEIGHT)}
#     for wall in get_maze_at_time(TIME):
#         maze[wall] = False
#     bytes = deque(a:=BYTE_LIST[TIME:], len(a))
#     current_time = TIME
#     while True:
#         current_time += 1
#         tile_changed = bytes.popleft()
#         maze[tile_changed] = False
#         time = solve_maze(maze)
#         if time == float('inf'):
#             print(f"Maze unsolvable at time {current_time}")
#             print(f"Tile changed: {tile_changed}")
#             break
part_one()
part_two()
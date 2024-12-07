from itertools import cycle
import copy
import time
data = open("input-data/day06.txt").readlines()
data = [x.strip() for x in data]
data = [list(x) for x in data]

def get_initial_position(lab_map):
    for index, line in enumerate(lab_map):
        if "^" in line:
            x, y = [line.index("^"), index]
            lab_map[y][x] ="X"
            return x, y

def is_valid(x, y, lab_map):
    if x > len(lab_map[0])-1 or y > len(lab_map)-1 or x < 0 or y < 0:
        return False
    return True

def get_next_step(x, y, direction):
    newx, newy = x, y
    if direction == "up":
        newy -= 1
    elif direction == "right":
        newx += 1
    elif direction == "down":
        newy += 1
    elif direction == "left":
        newx -= 1
    return newx, newy

def solve_maze(lab_map):
    directions = cycle(["up", "right", "down", "left"])
    direction = next(directions)
    x, y = get_initial_position(lab_map)
    turns = []
    while True:
        newx, newy = get_next_step(x, y, direction)
        if is_valid(newx, newy, lab_map):
            tile_type = lab_map[newy][newx]
            if tile_type == "#":
                turn = [direction, x, y]
                if turn in turns:
                    return len([i for j in lab_map for i in j if i == "X"]), False
                turns.append(turn)
                direction = next(directions)
            else:
                lab_map[newy][newx] = "X"
                x, y = newx, newy
        else:
            break
    return len([i for j in lab_map for i in j if i == "X"]), True


def part_two():
    answer = 0
    for obstacle_x in range(len(data[0])):
        for obstacle_y in range(len(data)):
            if solved_maze[obstacle_y][obstacle_x] != "X":
                continue
            lab_map = copy.deepcopy(data)
            if lab_map[obstacle_y][obstacle_x] == "^":
                continue
            lab_map[obstacle_y][obstacle_x] = "#"
            _, terminates = solve_maze(lab_map)
            if not terminates:
                answer += 1
    return answer

solved_maze = copy.deepcopy(data)
part_one, _ = solve_maze(solved_maze)
print(f"Part one: {part_one}")
start = time.time()
answer = part_two()
end = time.time()
print(f"Part two: {answer}")
print(f"Time taken for part two: {end - start}") # takes roughly 20 seconds on my machine
from itertools import cycle
data = open("input-data/day06.txt").readlines()
data = [x.strip() for x in data]
data = [list(x) for x in data]
lab_map = data.copy()

def get_initial_position():
    for index, line in enumerate(lab_map):
        if "^" in line:
            x, y = [line.index("^"), index]
            lab_map[y][x] ="X"
            return x, y

def is_valid(x, y):
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

def part_one():
    directions = cycle(["up", "right", "down", "left"])
    direction = next(directions)
    x, y = get_initial_position()
    while True:
        newx, newy = get_next_step(x, y, direction)
        if is_valid(newx, newy):
            tile_type = lab_map[newy][newx]
            if tile_type == "#":
                direction = next(directions)
            else:
                lab_map[y][x] = "X"
                x, y = newx, newy
        else:
            break
    return len([x for y in lab_map for x in y if x == "X"]) + 1 # lazy lol

print(f"Part one: {part_one()}")

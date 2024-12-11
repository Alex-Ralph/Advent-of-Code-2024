data = open("input-data/day10.txt").read()
park_map = {x + 1j * y: int(val) for y, line in enumerate(data.split("\n"))
       for x, val in enumerate(line)}

map_width = len([x for x in park_map if x.real == 0])
map_height = len([x for x in park_map if x.imag == 0])

def get_surroundings(coord):
    surrounding_operations = [1j, -1j, 1, -1]
    for coord in [x + coord for x in surrounding_operations]:
        if 0 <= coord.real < map_width and 0 <= coord.imag < map_height:
            yield coord

def check_paths(coord):
    surroundings = list(get_surroundings(coord))
    valid_moves = [x for x in surroundings if park_map[x] == park_map[coord] + 1]
    if not valid_moves:
        yield None
    elif park_map[coord] == 8:
        for end_node in valid_moves:
            yield end_node
    else:
        for end_node in (subpath for x in valid_moves for subpath in check_paths(x)):
            if end_node is None:
                continue
            yield end_node


def get_trailhead_score(coord):
    end_nodes = list(check_paths(coord))
    unique_end_nodes = list(set(end_nodes))
    return len(unique_end_nodes)

def get_trailhead_rating(coord):
    end_nodes = list(check_paths(coord))
    return len(end_nodes)

def part_x(func):
    trail_starts = [coord for coord in park_map.keys() if park_map[coord] == 0]
    scores = [func(x) for x in trail_starts]
    return sum(scores)

def part_one():
    return part_x(get_trailhead_score)

def part_two():
    return part_x(get_trailhead_rating)

print(f"Part one: {part_one()}")
print(f"Part two: {part_two()}")
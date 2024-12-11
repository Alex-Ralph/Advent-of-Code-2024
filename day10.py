from collections.abc import Callable, Generator
data = open("input-data/day10.txt").read()
park_map = {x + 1j * y: int(val) for y, line in enumerate(data.split("\n"))
       for x, val in enumerate(line)}

map_width = sum(1 for x in park_map if x.real == 0)
map_height = sum(1 for x in park_map if x.imag == 0)

def get_surroundings(coord: complex) -> Generator[complex]:
    """get in-bound coordinates of input coord"""
    surrounding_operations = [1j, -1j, 1, -1]
    for coord in [x + coord for x in surrounding_operations]:
        if 0 <= coord.real < map_width and 0 <= coord.imag < map_height:
            yield coord

def check_paths(coord: complex) -> Generator[complex]:
    """For a given coordinate, finds all valid paths to a summit (9)"""
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

def get_trailhead_score(coord: complex) -> int:
    """Returns the count of unique summits reachable from the input coordinate"""
    end_nodes = list(check_paths(coord))
    unique_end_nodes = list(set(end_nodes))
    return len(unique_end_nodes)

def get_trailhead_rating(coord: complex) -> int:
    """Returns the count of all possible paths from the input coordinate to a summit"""
    end_nodes = list(check_paths(coord))
    return len(end_nodes)

def part_x(func: Callable[[complex], int]) -> int:
    """Calls func on each starting coordinate in the map, returns the sum of func(starting_coordinate)"""
    trail_starts = [coord for coord in park_map.keys() if park_map[coord] == 0]
    scores = [func(x) for x in trail_starts]
    return sum(scores)

print(f"Part one: {part_x(get_trailhead_score)}")
print(f"Part two: {part_x(get_trailhead_rating)}")
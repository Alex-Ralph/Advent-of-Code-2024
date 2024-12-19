data = open("input-data/day12.txt").read()
garden = {x + 1j * y: val for y, line in enumerate(data.split("\n"))
       for x, val in enumerate(line)}
garden_width = sum(1 for x in garden if x.real == 0)
garden_height = sum(1 for x in garden if x.imag == 0)

def is_valid_coordinate(coord: complex):
    return True if 0 <= coord.real < garden_width and 0 <= coord.imag < garden_height else False

def get_valid_neighbours(coord: complex) -> list[complex]:
    return [x for x in [coord+1, coord-1, coord+1j, coord-1j]
            if is_valid_coordinate(x)]

def get_region(coord, garden_copy):
    region = [coord]
    val = garden_copy[coord]
    garden_copy[coord] = "."
    for x in get_valid_neighbours(coord):
        if garden_copy[x] == val:
            [region.append(y) for y in get_region(x, garden_copy)]
    return region

def get_regions():
    garden_copy = garden.copy()
    regions = []
    for x in garden_copy:
        if garden_copy[x] != ".":
            regions.append(get_region(x, garden_copy))
    return regions

def get_perimeter(region: list[complex]) -> int:
    perimeter = 0
    for coord in region:
        all_neighbours = [coord+1, coord-1, coord+1j, coord-1j]
        perimeter += sum(1 for neighbour in all_neighbours
                        if neighbour not in get_valid_neighbours(coord)
                        or garden[neighbour] != garden[coord])
    return perimeter

def region_pricing(region: list[complex]) -> int:
    return get_perimeter(region) * len(region)

def part_one():
    regions = get_regions()
    return sum(region_pricing(region) for region in regions)


def get_top_coords(region: list[complex]):
    return [x for x in region if not is_valid_coordinate(x-1j) or garden[x-1j] != garden[x]]

def get_bottom_coords(region: list[complex]):
    return [x for x in region if not is_valid_coordinate(x+1j) or garden[x+1j] != garden[x]]

def get_left_coords(region: list[complex]):
    return [x for x in region if not is_valid_coordinate(x-1) or garden[x-1] != garden[x]]

def get_right_coords(region: list[complex]):
    return [x for x in region if not is_valid_coordinate(x+1) or garden[x+1] != garden[x]]

def get_edge_count(initial_coords: list[complex], vertical=False) -> int:
    if len(initial_coords) == 1:
        return 1
    axes = [lambda x: x.imag, lambda x: x.real]
    if vertical:
        axes = axes[::-1]
    first_coord = initial_coords[0]
    edge_coords = [x for x in initial_coords if axes[0](x) == axes[0](first_coord)]
    if len(edge_coords) == 1:
        remaining = initial_coords[1:]
        return 1 + get_edge_count(remaining, vertical)
    edge_coords.sort(key=axes[1])
    edge_count = 1
    for index, edge in enumerate(edge_coords[:-1]):
        if axes[1](edge_coords[index+1]) - 1 != axes[1](edge):
            edge_count += 1
    remaining = [x for x in initial_coords if x not in edge_coords]
    if remaining:
        return get_edge_count(remaining, vertical) + edge_count
    return edge_count

def part_two():
    total = 0
    regions = get_regions()
    for region in regions:
        edges = 0
        edges += get_edge_count(get_top_coords(region))
        edges += get_edge_count(get_bottom_coords(region))
        edges += get_edge_count(get_left_coords(region), True)
        edges += get_edge_count(get_right_coords(region), True)
        total += edges * len(region)

    return total


print(f"Part one: {part_one()}")
print(f"Part two: {part_two()}")
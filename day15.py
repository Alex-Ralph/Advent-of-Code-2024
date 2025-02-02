def parse_data(big_map=False):
    floor_string = open("input-data/day15-map.txt").read()
    moves_string = open("input-data/day15-moves.txt").read()
    if big_map:
        floor_string = floor_string.replace("#", "##")
        floor_string = floor_string.replace(".", "..")
        floor_string = floor_string.replace("O", "[]")
        floor_string = floor_string.replace("@", "@.")
    floor_map = {x + 1j * y: val for y, line in enumerate(floor_string.split("\n"))
                 for x, val in enumerate(line)}
    instructions = [x for x in moves_string]
    return floor_map, instructions
    
def check_vertical_move(floor_map: dict[complex: str], source: complex, movement_vector: complex) -> bool:
    destination = source + movement_vector
    match floor_map[destination]:
        case ".":
            return True
        case "#":
            return False
        case "[":
            return (check_vertical_move(floor_map, destination, movement_vector) and
                    check_vertical_move(floor_map, destination+1, movement_vector))
        case "]":
            return (check_vertical_move(floor_map, destination, movement_vector) and 
                    check_vertical_move(floor_map, destination-1, movement_vector))


def make_move(floor_map: dict[complex: str], source: complex, movement_vector: complex) ->  bool:
    """ Moves an item from the source tile to the destination tile
    If the destination tile also contains an item, it will try to move that as well
    Returns True if the move is successfully made, and False if the move cannot be made
    Also edits the floor_map to reflect these changes
    """
    destination = source + movement_vector
    if floor_map[destination] == ".":
        floor_map[destination] = floor_map[source]
        floor_map[source] = "."
        return True
    elif floor_map[destination] == "#":
        return False
    elif floor_map[destination] == "O":
        can_move = make_move(floor_map, destination, movement_vector)
        if can_move:
            floor_map[destination] = floor_map[source]
            floor_map[source] = "."
            return True
        return False
    elif floor_map[destination] == "[" or floor_map[destination] == "]":
        if move_big_box(floor_map, destination, movement_vector):
            floor_map[destination] = floor_map[source]
            floor_map[source] = "."
            return True
        return False

def move_big_box(floor_map: dict[complex: str], source: complex, movement_vector: complex) -> bool:
    destination = source+movement_vector
    match movement_vector:
        case 1 | -1:
            if make_move(floor_map, source+movement_vector, movement_vector):
                floor_map[source+movement_vector] = floor_map[source]
                floor_map[source] = "."
                return True
            return False
        case 1j | -1j:
            offset = 1 if floor_map[source] == "[" else -1
            if (check_vertical_move(floor_map, source, movement_vector) and
                check_vertical_move(floor_map, source+offset, movement_vector)):
                make_move(floor_map, source, movement_vector)
                make_move(floor_map, source+offset, movement_vector)
                return True
            return False

def convert_direction(dir: str):
    match dir:
        case "^":
            return -1j
        case "v":
            return 1j
        case ">":
            return 1
        case "<":
            return -1
        case _:
            print("Tried to match " + dir)

def print_map(floor_map: dict[complex: str], bot_location: complex=None):
    """For debugging"""
    new_map = floor_map.copy()
    if bot_location:
        new_map[bot_location] = "@"
    map_height = sum(1 for x in new_map.keys() if x.real == 0)
    for y in range(map_height):
        print(''.join([val for key, val in new_map.items() if key.imag == y]))
        pass

def solve(floor_map: dict[complex], instructions: list[str]) -> int:
    robot_location = [key for key, value in floor_map.items() if value == "@"][0]
    floor_map[robot_location] = "."
    for direction in instructions:
        vector = convert_direction(direction)
        move_made = make_move(floor_map, robot_location, vector)
        if move_made:
            robot_location = robot_location + vector
    
    gps_total = sum(100 * key.imag + key.real for key, value in floor_map.items() 
                    if value in ["O", "["])
    return int(gps_total)

floor_map, insts = parse_data()
print(f"Part one: {solve(floor_map, insts)}")
floor_map, insts = parse_data(True)
print(f"Part two: {solve(floor_map, insts)}")
import math
input = open("input-data/day08.txt").read()
data = {x + 1j * y: val for y, line in enumerate(input.split("\n"))
        for x, val in enumerate(line)}

towers = {}
for coord, val in data.items():
        if val != ".":
           towers.update({coord: val})

width = len([x for x in data if x.real == 0])
height = len([x for x in data if x.imag == 0])

def valid_coord(coord: complex) -> bool:
    return (0 <= coord.real <= width-1) and (0 <= coord.imag <= height-1)


def part_one():
    antinodes = []
    for tower_one, val_one in towers.items():
        for tower_two, val_two in towers.items():
            if tower_one == tower_two:
                continue
            if val_one == val_two:
                antinode = tower_two + (tower_two - tower_one)
                if antinode not in antinodes:
                    antinodes.append(antinode)
    relevant_antinodes = [x for x in antinodes if valid_coord(x)]
    return len(relevant_antinodes)

def distance_to_vector(distance: complex):
    divisor = math.gcd(int(distance.real), int(distance.imag))
    return distance / divisor


def part_two():
    antinodes = []
    for tower_one, val_one in towers.items():
        for tower_two, val_two in towers.items():
            if tower_one == tower_two:
                continue
            if val_one == val_two:
                vector = distance_to_vector(tower_two - tower_one)
                mult = 0
                while True:
                    new_coord = tower_one + mult * vector
                    if not valid_coord(new_coord):
                        break
                    if new_coord not in antinodes:
                        antinodes.append(new_coord)
                    mult += 1
                while True:
                    new_coord = tower_one - mult * vector
                    if not valid_coord(new_coord):
                        break
                    if new_coord not in antinodes:
                        antinodes.append(new_coord)
                    mult += 1
    return len(antinodes)

print(f"Part one: {part_one()}")
print(f"Part two: {part_two()}")
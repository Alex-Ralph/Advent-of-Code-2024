import functools

def parse_data():
    with open("input-data/day19.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        towels = lines[0].split(", ")
        return towels, lines[2:]

@functools.cache
def build_pattern(pattern):
    for towel in towels: 
        if towel == pattern:
            return True
        if pattern.startswith(towel):
            if build_pattern(pattern[len(towel):]):
                return True
    return False

towels, patterns = parse_data()

def part_one():
    out = len([x for x in patterns if build_pattern(x)])
    print(out)

@functools.cache
def count_builds(pattern):
    count = 0
    for towel in towels:
        if towel == pattern:
            count += 1
        if pattern.startswith(towel):
            count += count_builds(pattern[len(towel):])
    return count

def part_two():
    print(sum([count_builds(x) for x in patterns]))
    
part_one()
part_two()
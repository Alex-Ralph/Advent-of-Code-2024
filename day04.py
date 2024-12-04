import re
data = [x.strip() for x in open("input-data/day04.txt").readlines()]

def find_xmas(line: str) -> int:
    """searches for instances of the word 'xmas'. Searches forwards and backwards"""
    return len(re.findall(r'(XMAS)', line)) + len(re.findall(r'(SAMX)', line))

def transpose(wordsearch: list[str]) -> list[str]:
    """rotates the wordsearch 90 degrees"""
    return [''.join(list(x)) for x in zip(*wordsearch)]

def find_diagonals(wordsearch: list[str]) -> list[str]:
    """returns all left-right diagonals of the wordsearch"""
    width = len(wordsearch[0])
    height = len(wordsearch)
    diagonals = []
    for index in range(width):
        diagonal = []
        y = 0
        x = index
        while y < height and x < width:
            diagonal.append(wordsearch[y][x])
            y += 1
            x += 1
        diagonals.append(''.join(diagonal))
    for index in range(1, height):
        diagonal = []
        y = index 
        x = 0
        while y < height and x < width:
            diagonal.append(wordsearch[y][x])
            y += 1
            x += 1
        diagonals.append(''.join(diagonal))
    return diagonals

def part1() -> int:
    transposed = transpose(data)
    diagonals = find_diagonals(data)
    more_diagonals = find_diagonals(list(reversed(data)))
    lines = data + transposed + diagonals + more_diagonals
    return sum([find_xmas(x) for x in lines])

def check_surroundings(line_no: int, col_no: int) -> bool:
    diag_1 = data[line_no-1][col_no-1] + data[line_no+1][col_no+1]
    diag_2 = data[line_no-1][col_no+1] + data[line_no+1][col_no-1]
    if diag_1 in ["SM", "MS"] and diag_2 in ["SM", "MS"]:
        return True
    return False

def part2() -> int:
    x_count = 0
    for i, line in enumerate(data[1:-1]):
        for j, char in enumerate(line[1:-1]):
            if char == 'A' and check_surroundings(i+1, j+1):
                x_count += 1
    return x_count

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")


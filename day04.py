import re
data = [x.strip() for x in open("input-data/day04.txt").readlines()]

def find_xmas(line: str) -> int:
    """searches for instances of the word 'xmas'. Searches forwards and backwards"""
    return len(re.findall(r'(XMAS)', line)) + len(re.findall(r'(SAMX)', line))

def transpose(wordsearch: list[str]) -> list[str]:
    """rotates the wordsearch 90 degrees"""
    return [''.join(list(x)) for x in zip(*wordsearch)]

def find_diagonal(wordsearch: list[str], x: int, y: int) -> str:
    """Given an x, y coordinate of a letter in a wordsearch, returns
    the string heading down+right diagonally"""
    width = len(wordsearch[0])
    height = len(wordsearch)
    diagonal = ""
    while y < height and x < width:
        diagonal += wordsearch[y][x]
        y+= 1
        x += 1
    return diagonal

def find_diagonals(wordsearch: list[str]) -> list[str]:
    """returns all left-right diagonals of the wordsearch"""
    diagonals = []
    for index in range(len(wordsearch[0])):
        diagonals.append(find_diagonal(wordsearch, index, 0))
    for index in range(1, len(wordsearch)):
        diagonals.append(find_diagonal(wordsearch, 0, index))
    return diagonals

def part1() -> int:
    transposed = transpose(data)
    diagonals = find_diagonals(data)
    more_diagonals = find_diagonals(list(reversed(data)))
    lines = data + transposed + diagonals + more_diagonals
    return sum([find_xmas(x) for x in lines])

def check_surroundings(line_no: int, col_no: int) -> bool:
    """Checks the diagonals of a given char in 'data' to see if,
    given that the input character is an 'A', the character is the center
    of an X-MAS
    """
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


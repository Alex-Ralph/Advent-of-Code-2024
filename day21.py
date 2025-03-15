"""Initial plan:
1. Write a function that can, for a start and end point, calculate all the shortest routes
2. Write this for the other type of keypad
3. Link these together such that for each path in keypad a, we find all the paths in keypad b that would lead to those, and then in keypad c we do the same
find the smallest path in keypad c
If we cache results the calculations will be a lot faster"""
from functools import cache
import re
INPUT_FILE = "input-data/day21.txt"

def parse_data() -> list[str]:
    with open(INPUT_FILE) as file:
        return [x.strip() for x in file.readlines()]

numeric_layout = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    [None, 0, "A"]
]
numeric_layout = [[str(x) for x in y] for y in numeric_layout]
directional_layout = [
    ["None", "^", "A"],
    ["<", "v", ">"]
]

class Keypad():
    def __init__(self, layout: list[list[str]]):
        self.layout = layout

    @cache
    def _get_shortest_paths(self, start: tuple[int, int], end: tuple[int, int]) -> list[str]:
        paths = []
        if start == end:
            return [""]
        if start[0] != end[0]:
            y = start[0]+1 if start[0] < end[0] else start[0]-1
            move = "v" if start[0] < end[0] else "^"
            if self.layout[y][start[1]] != "None":
                for path in self._get_shortest_paths((y, start[1]), end):
                    paths.append(move+path)
        if start[1] != end[1]:
            x = start[1]+1 if start[1] < end[1] else start[1]-1
            if self.layout[start[0]][x] != "None":
                move = ">" if start[1] < end[1] else "<"
                for path in self._get_shortest_paths((start[0], x), end):
                    paths.append(move+path)
        return paths

    @cache
    def get_location(self, button: str) -> tuple[int, int]:
        for y, row in enumerate(self.layout):
            for x, val in enumerate(row):
                if val == button:
                    return (y, x)
        return None

    @cache
    def get_shortest_paths(self, start: str, end: str) -> list[str]:
        start_loc = self.get_location(start)
        end_loc = self.get_location(end)
        return self._get_shortest_paths(start_loc, end_loc)

    @cache
    def get_paths_for_sequence(self, inputs: str, start="A") -> list[str]:
        prev_char = start
        paths=[""]
        for char in inputs:
            new_paths = []
            for shortest_path in self.get_shortest_paths(prev_char, char):
                for path in paths:
                    new_paths.append(path + shortest_path + "A")
            paths = new_paths
            prev_char=char
        return paths

    @cache
    def find_all_shortest(self, inputs: tuple[str]) -> list[str]:
        shortest = float('inf')
        out = []
        for input in inputs:
            for path in self.get_paths_for_sequence(input):
                if len(path) > shortest:
                    continue
                elif len(path) == shortest:
                    out.append(path)
                else:
                    out = [path]
                    shortest = len(path)
        return out

    def decode(self, path: str) -> str:
        """Finds what the output will be if you enter a string of commands"""
        position = list(self.get_location("A"))
        out = ""
        for char in path:
            match char:
                case "^":
                    position[0] -= 1
                case "v":
                    position[0] += 1
                case "<":
                    position[1] -= 1
                case ">":
                    position[1] += 1
                case "A":
                    out += self.layout[position[0]][position[1]]
        return out

def part_one():
    numeric_pad = Keypad(numeric_layout)
    directional_pad = Keypad(directional_layout)
    codes = parse_data()
    complexities = 0
    for code in codes:
        numeric_paths = numeric_pad.get_paths_for_sequence(code)
        inner_directional_paths = directional_pad.find_all_shortest(tuple(numeric_paths))
        outer_directional_paths = directional_pad.find_all_shortest(tuple(inner_directional_paths))
        complexities += len(outer_directional_paths[0]) * int(code[:-1])
    print(complexities)

def part_two():
    """Is there some sort of mathematical rule we can use to remove A-presses, or calculate how much
    larger it will be for each directional pad?
    Each time you press a key you have to double the journey to go back to the A button, is that something?"""
    numeric_pad = Keypad(numeric_layout)
    directional_pad = Keypad(directional_layout)
    codes = parse_data()
    complexities = 0
    for code in codes:
        shortest_paths = numeric_pad.get_paths_for_sequence(code)
        for i in range(25):
            print(f"i: {i}")
            shortest_paths = directional_pad.find_all_shortest(tuple(shortest_paths))
        complexities += len(shortest_paths[0] * int(code[:-1]))
    print(complexities)

part_one()
# part_two()
numeric_pad = Keypad(numeric_layout)
directional_pad = Keypad(directional_layout)
codes = ["<"]
complexities = 0
for code in codes:
    shortest_paths = codes
    for i in range(6):
        print(f"i: {i}")
        shortest_paths = directional_pad.find_all_shortest(tuple(shortest_paths))
        print(len(shortest_paths[0]))
    complexities += len(shortest_paths[0] * int(code[:-1]))
print(complexities)

"""Each arrow has a "cost" and you always end up having to move from A, to the arrow, back to A.
Is thare a reliable value you could multiply each arrow by?"""
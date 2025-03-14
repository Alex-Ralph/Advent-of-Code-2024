"""Initial plan:
1. Write a function that can, for a start and end point, calculate all the shortest routes
2. Write this for the other type of keypad
3. Link these together such that for each path in keypad a, we find all the paths in keypad b that would lead to those, and then in keypad c we do the same
find the smallest path in keypad c
If we cache results the calculations will be a lot faster"""

INPUT_FILE = "test-data/day21.txt"

def parse_data() -> list[str]:
    with open(INPUT_FILE) as file:
        return [x for x in file.readlines()]

numeric_keypad = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    [None, 0, "A"]
]
numeric_keypad = [[str(x) for x in y] for y in numeric_keypad]
directional_keypad = [
    [None, "^", "A"],
    ["<", "v", ">"]
]

class Keypad():
    def __init__(self, layout: list[list[str]]):
        self.layout = layout

    @staticmethod
    def _get_shortest_paths(start: tuple[int, int], end: tuple[int, int]) -> list[str]:
        paths = []
        if start == end:
            return [""]
        if start[0] != end[0]:
            y = start[0]+1 if start[0] < end[0] else start[0]-1
            move = "v" if start[0] < end[0] else "^"
            for path in Keypad._get_shortest_paths((y, start[1]), end):
                paths.append(move+path)
        if start[1] != end[1]:
            x = start[1]+1 if start[1] < end[1] else start[1]-1
            move = ">" if start[1] < end[1] else "<"
            for path in Keypad._get_shortest_paths((start[0], x), end):
                paths.append(move+path)
        return paths

    def get_location(self, button: str) -> tuple[int, int]:
        for y, row in enumerate(self.layout):
            for x, val in enumerate(row):
                if val == button:
                    return (y, x)
        return None

    def get_shortest_paths(self, start: str, end: str) -> str:
        start_loc = self.get_location(start)
        end_loc = self.get_location(end)
        return Keypad._get_shortest_paths(start_loc, end_loc)

test_pad = Keypad(numeric_keypad)
print(test_pad.get_shortest_paths("2", "9"))

# def part_one():

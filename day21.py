"""
This solution could definitely be a lot shorter.
It's solved though, so I'm moving on :)
"""
from functools import cache
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
    def get_location(self, button: str) -> tuple[int, int]:
        """Get coordinates of a button on the keypad"""
        for y, row in enumerate(self.layout):
            for x, val in enumerate(row):
                if val == button:
                    return (y, x)
        return None

    @cache
    def _get_shortest_paths(self, start: tuple[int, int], end: tuple[int, int]) -> list[str]:
        """For a starting coordinate and ending coordinate,
        returns all possible shortest paths from one to the other"""
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
    def get_shortest_paths(self, start: str, end: str) -> list[str]:
        """Return all shortest paths from one character to another"""
        start_loc = self.get_location(start)
        end_loc = self.get_location(end)
        return self._get_shortest_paths(start_loc, end_loc)

    @cache
    def get_paths_for_sequence(self, inputs: str, start="A") -> list[str]:
        """Get all paths for a given sequence of buttons"""
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
    def score_move(self, start: str, end: str, robot_count: int):
        paths = self.get_shortest_paths(start, end)
        paths = [x + "A" for x in paths]
        if robot_count == 1:
            return len(paths[0])
        lowest_cost = float('inf')
        for path in paths:
            score = 0
            moves = list(zip("A" + path[:-1], path))
            for start, end in moves:
                score += self.score_move(start, end, robot_count - 1)
            lowest_cost = score if score < lowest_cost else lowest_cost
        return lowest_cost

    def score_sequence(self, sequence: str, robot_count: int):
        moves = list(zip("A" + sequence[:-1], sequence))
        score = sum([self.score_move(a, b, robot_count) for a, b in moves])
        return score

def solve(robots: int):
    numeric_pad = Keypad(numeric_layout)
    directional_pad = Keypad(directional_layout)
    data = parse_data()
    out=0
    for code in data:
        initial_paths = numeric_pad.get_paths_for_sequence(code)
        scores = [
            directional_pad.score_sequence(x, robots)
            for x in initial_paths
        ]
        lowest_score = min(scores)
        out += lowest_score * int(code[:-1])
    print(out)

solve(2)
solve(25)
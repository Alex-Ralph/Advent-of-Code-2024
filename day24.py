from copy import copy, deepcopy
from itertools import combinations, permutations
class Wire():
    def __init__(self, inputs: list[str], output: str, operation: str) -> None:
        self.inputs = inputs
        self.output = output
        self.operation = operation
        self.value = None

    def solve(self, gates):
        input_values = tuple((gates[x] for x in self.inputs))
        match self.operation:
            case "OR":
                if any(input_values):
                    self.value = True
                elif all((x is False for x in input_values)):
                    self.value = False
            case "AND":
                if all(input_values):
                    self.value = True
                if False in input_values:
                    self.value = False
            case "XOR":
                if True in input_values and False in input_values:
                    self.value = True
                elif not None in input_values:
                    self.value = False
        if self.value is not None:
            gates[self.output] = self.value
            return True
        return False

def parse_data() -> tuple[dict[str: bool], tuple[Wire]]:
    with open("input-data/day24.txt") as file:
        lines = file.read()
        init_lines, wire_lines = lines.split("\n\n")
        init_lines = init_lines.split("\n")
        wire_lines = wire_lines.split("\n")
        gate_dict = {x: bool(int(y)) for a in init_lines for x, y in [a.split(": ")]}
        wire_values = [x.split(" ") for x in wire_lines]
        for x in wire_values:
            gate_dict[x[-1]] = None
        wires = []
        for wire_val in wire_values:
            wire_val.remove("->")
            wires.append(Wire((wire_val[0], wire_val[2]), wire_val[-1], wire_val[1]))
        return gate_dict, wires

class Breadboard():
    def __init__(self):
        self.init_gates, self.wires = parse_data()
        self.reset()

    def reset(self):
        self.gates = copy(self.init_gates)
        for x in self.wires:
            x.value = None

    def solve_gates(self):
        while self.wires:
            solved_wires = [x for x in self.wires if x.solve(self.gates) == True]
            for x in solved_wires:
                self.wires.remove(x)
            if len(solved_wires) == 0:
                break

    def swap_outputs(self, wire_a_index: int, wire_b_index: int):
        x = self.wires[wire_a_index].output
        self.wires[wire_a_index].output = self.wires[wire_b_index].output
        self.wires[wire_b_index].output = x

    def get_binary_value(self, gate_letter: str) -> int:
        output_gates = sorted([x for x in self.gates if x[0] == gate_letter], reverse=True)
        return int("".join(str(int(self.gates[x])) for x in output_gates), 2)

def part_one():
    board = Breadboard()
    board.solve_gates()
    print(board.get_binary_value("z"))

def find_valuable_swaps(target_value: str, initial_value: str, board: Breadboard,
                        unswapped_wires: list[Wire]) -> list[int]:
    """Could solve this recursively, keep stacking up changes to the same breadboard
    until we reach 8 swaps"""



def part_two():
    # Potential solutions
    # 1. for each pair, check if it gets closer to the answer.
    # Then for each pair that gets closer to the answer, iterate through
    # all the pairs again and see if they will get any closer
    # iterate until we have eight swaps and a solution

    # 2. For each z-value, find all the pairs that influence that value
    # work from here idk
    board = Breadboard()
    board.solve_gates()
    target_value = board.get_binary_value("x") + board.get_binary_value("y")
    target_string = f"{target_value:b}"
    initial_string = f'{board.get_binary_value("z"):b}'
    initial_diff_count = sum(1 for x, y in zip(target_string, initial_string) if x != y)
    possible_swaps = combinations(list(range(len(board.init_wires))), 2)
    board.reset()
    valuable_swaps = []
    for swap in possible_swaps:
        board.swap_outputs(swap[0], swap[1])
        new_result = f'{board.get_binary_value("z"):b}'
        diff_count = sum(1 for x, y in zip(target_string, new_result) if x != y)
        if diff_count < initial_diff_count:
            valuable_swaps.append(swap)
        board.reset()

part_one()
# part_two()

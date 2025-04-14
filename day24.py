from copy import copy, deepcopy
from itertools import  permutations
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

def solve_gates(gates: dict[str: bool], wires: tuple[Wire]) -> None:
    wires = deepcopy(wires)
    while wires:
        solved_wires = [x for x in wires if x.solve(gates) == True]
        for x in solved_wires:
            wires.remove(x)
        if len(solved_wires) == 0:
            break


def part_one():
    gates, wires = parse_data()
    solve_gates(gates, wires)
    z_values = [x for x in gates if x[0] == 'z']
    z_values.sort(reverse=True)
    binary = "".join(str(int(gates[x])) for x in z_values)
    print(int(binary, 2))

def part_two():
    # This would work eventually, in a few thousand years
    # My instinct is to work out which gates change which values of z
    gates, wires = parse_data()
    output_gates = [sorted([x for x in gates if x[0] == char], reverse=True) for char in ("x", "y", "z")]
    perms = permutations(wires, 8)
    for permutation in perms:
        new_gates = copy(gates)
        for i in range(0,len(permutation),2):
            x = permutation[i].output
            permutation[i].output = permutation[i+1].output
            permutation[i+1].output = x
        solve_gates(new_gates, wires)
        for i in range(0,len(permutation),2):
            x = permutation[i].output
            permutation[i].output = permutation[i+1].output
            permutation[i+1].output = x
        if any([True for y in output_gates for x in y if new_gates[x] is None]):
            continue # not all x, y, and z gates have values
        binary_values = []
        for x in output_gates:
            binary_string = "".join(str(int(new_gates[y])) for y in x)
            binary_values.append(int(binary_string, 2))
        if binary_values[0] + binary_values[1] == binary_values[2]:
            print(",".join(sorted([x.output for x in permutation])))
            break

part_one()
part_two()

from copy import copy
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
    with open("test-data/day24.txt") as file:
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

def part_one():
    gates, wires = parse_data()
    while wires:
        solved_wires = [x for x in wires if x.solve(gates) == True]
        for x in solved_wires:
            wires.remove(x)
    z_values = [x for x in gates if x[0] == 'z']
    z_values.sort(reverse=True)
    binary = "".join(str(int(gates[x])) for x in z_values)
    print(int(binary, 2))

def part_two():
    gates, wires = parse_data()
    SWAPPED_WIRES = 2
    for wire_one in wires:
        wire_one_init = wire_one.output
        for wire_two in wires:
            if wire_one == wire_two:
                continue
            wire_one.output = wire_two.output
            wire_two.output = wire_one_init



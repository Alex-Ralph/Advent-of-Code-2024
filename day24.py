def parse_data():
    with open("test-data/day24.txt") as file:
        lines = file.read()
        init_lines, gate_lines = lines.split("\n\n")
        init_values = [x.split(": ") for x in init_lines.split("\n")]
        gates = [x.split(" ") for x in gate_lines.split("\n")]
        for x in gates: del x[3]
        return init_values, gates

print(parse_data())
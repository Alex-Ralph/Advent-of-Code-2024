from typing import Generator
from copy import copy
# This whole file is ugly and I don't like it. Would not push to prod.

def parse_data() -> tuple[dict[str: bool|None], list[list[str]]]:
    with open("test-data/day24.txt") as file:
        lines = file.read()
        init_lines, wire_lines = lines.split("\n\n")
        init_lines = init_lines.split("\n")
        wire_lines = wire_lines.split("\n")
        init_vals = [x.split(": ") for x in init_lines]
        wires = [x.split(" ") for x in wire_lines]
        for wire in wires:
            wire.remove("->")
        unique_pins = set([x[0] for x in init_vals] + [wire[0] for wire in wires] + [x for wire in wires for x in (wire[0], wire[2], wire[3])])
        pin_maps = {pin: None for pin in unique_pins}
        for val in init_vals:
            pin_maps[val[0]] = bool(int(val[1]))
        return pin_maps, wires

def solve_wire(wire_string: list[str], pin_maps: dict[str: bool|None]):
    left_pin, op, right_pin, out = wire_string
    lhs = pin_maps[left_pin]
    rhs = pin_maps[right_pin]
    match op:
        case "OR":
            if any((lhs, rhs)):
                pin_maps[out] = True
                return True
            if lhs is False and rhs is False:
                pin_maps[out] = False
                return True
        case "AND":
            if all((lhs, rhs)):
                 pin_maps[out] = True
                 return True
            if False in ((lhs, rhs)):
                pin_maps[out] = False
                return True
        case "XOR":
            if True in ((lhs, rhs)) and False in ((lhs, rhs)):
                pin_maps[out] = True
                return True
            if not None in ((lhs, rhs)):
                pin_maps[out] = False
                return True

def solve(wires: list[list[[str]]], pin_maps: dict[str: bool|None]) -> None:
    """Edits pin_maps in place"""
    while wires:
        pins_solved = [(x, solve_wire(x, pin_maps)) for x in wires]
        for x in pins_solved:
            if x[1]:
                wires.remove(x[0])

def part_one():
    pin_maps, wires = parse_data()
    solve(wires, pin_maps)
    while wires:
        pins_solved = [(x, solve_wire(x, pin_maps)) for x in wires]
        for x in pins_solved:
            if x[1]:
                wires.remove(x[0])
    z_list = [str(int(pin_maps[x])) for x in sorted(pin_maps.keys(), reverse=True) if x[0] == "z"]
    print(int("".join(z_list), 2))

def swap_wires(wires: list[list[str]]):
    for i in range(len(wires) - 1):
        for j in range(i+1, len(wires)):
            a=wires[i][3]
            wires[i][3] = wires[j][3]
            wires[j][3] = a
            yield (wires[i][3], wires[j][3])
            wires[j][3] = wires[i][3]
            wires[i][3] = a
    yield (None, None)

def part_two():
    """Grug solution: just keep swapping shit until it works
    Potentially better solution: Find out which wire will change which binary bits, and which binary bits need changing
    Start swapping the pins that will influence the correct binary bits
    Grug solution will be helpful for producing a method of swapping wires, so start with that and when it
    inevitably fails, try being smarter about it
    """
    pin_maps, wires = parse_data()
    for swaps in swap_wires(wires):
        for swaps_2 in swap_wires(wires):
            if any((x in swaps_2 for x in swaps)):
                continue
            result = copy(pin_maps)
            solve(copy(wires), result)
            x_list = [result[x] for x in sorted(result.keys(), reverse=True) if x[0] == "x" and result[x] is not None]
            y_list = [result[x] for x in sorted(result.keys(), reverse=True) if x[0] == "y" and result[x] is not None]
            z_list = [result[x] for x in sorted(result.keys(), reverse=True) if x[0] == "z" and result[x] is not None]
            if [] in [x_list, y_list, z_list]:
                continue
            x_strs = [str(int(x))for x in x_list]
            y_strs = [str(int(x)) for x in y_list]
            z_strs = [str(int(x)) for x in z_list]

            x_val = int("".join(x_strs), 2)
            y_val = int("".join(y_strs), 2)
            z_val = int("".join(z_strs), 2)
            if x_val & y_val == z_val:
                print(swaps, swaps_2)
                return

part_one()
part_two()
import numpy as np
import re

def parse_data():
    data = open("input-data/day13.txt").read()
    machine_text = data.split("\n\n")
    machines = [ClawMachine(x) for x in machine_text]
    return machines

class ClawMachine():
    def __init__(self, input_text: str):
        lines = input_text.split("\n")
        self.a_button = list(map(int, re.findall(r'(?<=\+)\d+', lines[0])))
        self.b_button = list(map(int, re.findall(r'(?<=\+)\d+', lines[1])))
        self.prize = list(map(int, re.findall(r'(?<=\=)\d+', lines[2])))

    def solve_simultaneous(self) -> list[float]:
        x_eq = [self.a_button[0], self.b_button[0]]
        y_eq = [self.a_button[1], self.b_button[1]]
        targets = [self.prize[0], self.prize[1]]
        solutions = np.linalg.solve([x_eq, y_eq], targets)
        return solutions
    
    def get_price(self) -> int:
        presses = self.solve_simultaneous()
        presses = np.rint(presses)
        # check if the solution is valid
        # necessary to guard against floating point errors
        if (self.a_button[0] * presses[0] + self.b_button[0] * presses[1] == self.prize[0] and 
                self.a_button[1] * presses[0] + self.b_button[1] * presses[1] == self.prize[1]):
            return int(3 * presses[0] + presses[1])
        return 0

def day_one():
    machines = parse_data()
    return sum(machine.get_price() for machine in machines)

def day_two():
    machines = parse_data()
    for machine in machines:
        machine.prize[0] += 10000000000000
        machine.prize[1] += 10000000000000
    return sum(machine.get_price() for machine in machines)
        
print(f"Day one: {day_one()}")
print(f"Day two: {day_two()}")

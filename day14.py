import re
import time
MAP_WIDTH = 101
MAP_HEIGHT = 103

def parse_data():
    return [Robot(x) for x in open("input-data/day14.txt").readlines()]

class Robot:
    def __init__(self, initial: str):
        vals = re.findall(r'-?\d+', initial)
        vals = [int(x) for x in vals]
        self.x = vals[0]
        self.y = vals[1]
        self.x_vel = vals[2]
        self.y_vel = vals[3]

    def get_position(self, time: int) -> list[list[int]]:
        x_movement = self.x + time*self.x_vel
        y_movement = self.y + time*self.y_vel
        new_x = abs(x_movement % MAP_WIDTH)
        new_y = abs(y_movement % MAP_HEIGHT)
        return [new_x, new_y]

    def find_repeat(self):
        i = 0
        x_pos = self.x
        y_pos = self.y
        while True:
            x_pos += abs(self.x_vel % MAP_WIDTH)
            y_pos += abs(self.y_vel % MAP_HEIGHT)
            i += 1
            if x_pos == self.x and y_pos == self.y:
                return i

def print_map(positions):
    for y in range(MAP_HEIGHT):
        line = ""
        for x in range(MAP_WIDTH):
            appearance_count = sum(1 for pos in positions if pos[0] == x and pos[1] == y)
            if appearance_count:
                line += str(appearance_count)
            else:
                line += "."
        print(line)

def part_one():
    robots = parse_data()
    positions = [robot.get_position(100) for robot in robots]
    mid_col = int((MAP_WIDTH+1)/2)
    mid_row = int((MAP_HEIGHT+1)/2)
    quad_ranges = [[range(mid_col-1), range(mid_row-1)], 
                   [range(mid_col-1), range(mid_row, MAP_HEIGHT)], 
                   [range(mid_col, MAP_WIDTH), range(mid_row-1)], 
                   [range(mid_col, MAP_WIDTH), range(mid_row, MAP_HEIGHT)]]
    total = 1
    for ranges in quad_ranges:
        quad_total = 0
        for x in ranges[0]:
            for y in ranges[1]:
                quad_total += sum([1 for pos in positions if pos[0] == x and pos[1] == y])
        total *= quad_total
    return total

def part_two():
    robots = parse_data()
    val = max([robot.find_repeat() for robot in robots])
    print(map([robot.get_position(val) for robot in robots]))
    print(val)

print(f"Part one: {part_one()}")
part_two()

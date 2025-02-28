import math
def parse_data():
    text = open("input-data/day17.txt").readlines()
    text.pop(3)
    return [x.split()[-1] for x in text]


class Processor:
    def __init__(self, a, b, c):
        self.init(a, b, c)
    
    def init(self, a, b, c):
        self.reg_a = int(a)
        self.reg_b =int(b)
        self.reg_c =int(c)
        self.instruction_pointer = 0
        self.output = []

    def combo_value(self, op):
        match op:
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6: 
                return self.reg_c
        if op > 6:
            raise ValueError("Invalid combo value")
        return op

    def run_instruction(self, inst, op):
        match inst: # division
            case 0:
                self.reg_a = int(self.reg_a / (2 ** self.combo_value(op)))
            case 1:
                self.reg_b = self.reg_b ^ op
            case 2:
                self.reg_b = self.combo_value(op) % 8
            case 3:
                if self.reg_a != 0:
                    self.instruction_pointer = op
                    return
            case 4:
                self.reg_b = self.reg_b ^ self.reg_c
            case 5:
                self.output.append(self.combo_value(op) % 8)
            case 6:
                self.reg_b = int(self.reg_a / (2 ** self.combo_value(op)))
            case 7:
                self.reg_c = int(self.reg_a / (2 ** self.combo_value(op)))
        self.instruction_pointer += 2

    def run(self, instructions: str | list[str]):
        if isinstance(instructions, str):
            inst_list = instructions.split(",")
            inst_list = [int(x) for x in inst_list]
        else:
            inst_list = instructions
        inst_count = len(inst_list)
        while self.instruction_pointer < inst_count:
            inst = inst_list[self.instruction_pointer]
            op = inst_list[self.instruction_pointer+1]
            self.run_instruction(inst, op)
        return self.output

    def reset(self, a=0, b=0, c=0):
        self.init(a,b,c)

def part_one():
    a,b,c,insts = parse_data()
    processor = Processor(a,b,c)
    out = processor.run(insts)
    print(",".join(out))

def part_two():
    _,_,_,insts = parse_data()
    inst_list = [int(x) for x in insts.split(",")]
    proc = Processor(0,0,0)
    power = len(inst_list) - 1
    a = 8 ** power
    while power >= 0:
        proc.reset(a)
        out = proc.run(insts)
        if out[power:] == inst_list[power:]:
            power -= 1
            continue
        relevant_digit = (a//(8**power) % 8)
        if relevant_digit == 7:
            a -= 7 * (8 ** power)
            power += 1
            a += 1 * (8 ** power)
            continue
        a += 8 ** power
    print(oct(a))
    print(a)
    proc.reset(a)
    print(proc.run(insts))

import time
data = open("input-data/day07.txt").readlines()
data = [x.strip() for x in data]

def eval_equation(running_total: int, others: list[int], target: int) -> bool:
    if running_total > target:
        return False
    if len(others) == 1:
        return (running_total + others[0] == target or running_total * others[0] == target)
    a = eval_equation(others[0] + running_total, others[1:], target)
    if running_total == 0:
        running_total = 1
    b = eval_equation(others[0] * running_total, others[1:], target)
    return a or b

def part_one():
    total = 0
    for line in data:
        line = line.split(":")
        target = int(line[0])
        numbers = [int(x) for x in line[1].split()]
        if eval_equation(0, numbers, target):
            total += target
    return total

def eval_with_concat(running_total: int, others: list[int], target: int) -> bool:
    if running_total > target:
        return False
    if len(others) == 1:
        last_val = others[0]
        add = last_val + running_total
        mult = last_val * running_total
        concat = int(f'{running_total}{last_val}')
        return (target in [add, mult, concat])
    add = eval_with_concat(others[0] + running_total, others[1:], target)
    if add:
        return True
    mult_total = running_total
    if mult_total == 0:
        mult_total = 1
    mult = eval_with_concat(others[0] * mult_total, others[1:], target)
    if mult:
        return True
    concat = int(str(running_total) + str(others[0]))
    concatenated = eval_with_concat(concat, others[1:], target)
    if concatenated:
        return True

def part_two():
    total = 0
    for line in data:
        line = line.split(":")
        target = int(line[0])
        numbers = [int(x) for x in line[1].split()]
        if eval_with_concat(0, numbers, target):
            total += target
    return total

print(f"Part one: {part_one()}")
start = time.time()
print(f"Part two: {part_two()}")
end = time.time()
print(f"Time taken: {end - start}")
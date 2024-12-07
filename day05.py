data = open("input-data/day05.txt").read()
sections = data.split("\n\n")
rules_text = sections[0].split("\n")
manual_lines = sections[1].split("\n")[:-1]
manuals = [x.split(",") for x in manual_lines]
rules = [[x[0], x[1]] for x in [y.split("|") for y in rules_text]]

def is_valid_manual(manual: list[str]) -> bool:
    for rule in rules:
        if rule[0] in manual and rule[1] in manual:
            if manual.index(rule[0]) > manual.index(rule[1]):
                return False
    return True

def part_one():
    valid_manuals = [x for x in manuals if is_valid_manual(x)]
    valid_totals = [x[int((len(x) - 1) / 2)] for x in valid_manuals]

    return sum(int(x) for x in valid_totals)

def fix_manual(manual: list[str]) -> list[str]:
    for rule in rules:
        if rule[0] in manual and rule[1] in manual:
            if manual.index(rule[0]) > manual.index(rule[1]):
                manual.remove(rule[0])
                manual.insert(manual.index(rule[1]), rule[0])
                manual = fix_manual(manual)
    return manual

def part_two():
    invalid_manuals = [x for x in manuals if not is_valid_manual(x)]
    fixed_manuals = [fix_manual(x) for x in invalid_manuals]
    fixed_totals = [x[int((len(x) - 1) / 2)] for x in fixed_manuals]
    return sum(int(x) for x in fixed_totals)

print(f"Part one: {part_one()}")
print(f"Part two: {part_two()}")

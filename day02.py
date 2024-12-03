

def check_safe(report: list[int]) -> bool:
    # Check list is sorted
    ascending = sorted(report)
    descending = sorted(report, reverse=True)
    if not ((ascending == report) or (descending == report)):
        return False

    # check no adjacent numbers are too different
    for id, x in enumerate(report[:-1]):
        diff = abs(report[id+1] - x)
        if diff == 0 or diff > 3:
            return False
    return True

data_str = open("input-data/day02.txt").readlines()
data = [[int(x) for x in line.split()] for line in data_str]

def part1():
    safe_reports = filter(check_safe, data)
    return sum(1 for _ in safe_reports)

def part2():
    safe_reports = 0
    for report in data:
        old_total = safe_reports
        if check_safe(report): 
            safe_reports += 1
            continue
        for x in range(len(report)):
            new_report = report.copy()
            new_report.pop(x)
            if check_safe(new_report):
                safe_reports += 1
                break
    return safe_reports


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")

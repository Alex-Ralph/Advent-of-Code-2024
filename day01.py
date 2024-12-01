datafile = "input-data/day01.txt"
datalines = open(datafile, "r").readlines()

def parse_data():
    a = [] 
    b = []
    for line in datalines:
        x = line.split()
        a.append(int(x[0]))
        b.append(int(x[1]))
    a.sort()
    b.sort()
    return a, b

def part1():
    a, b = parse_data() 
    data = zip(a, b)
    answer = sum([abs(x - y) for x, y in data])
    return answer

def part2():
    a, b = parse_data()
    answer = sum([x * b.count(x) for x in a])
    return answer

print(part1())
print(part2())

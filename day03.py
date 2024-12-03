import re
data = open("input-data/day03.txt").read().replace("\n",";")
def part_one(input):
    regex = r'(?<=mul\()\d{1,3},\d{1,3}(?=\))'
    muls = re.findall(regex, input)
    values = [int(x[0]) * int(x[1]) for x in [mul.split(',') for mul in muls]]
    return sum(values)

def part_two():
    dont_regex = r'(?<=don\'t\(\)).*?(?=do\(\))'
    new_data = ''.join(re.split(dont_regex, data))
    return part_one(new_data)


print(f"part 1: {part_one(data)}")
print(f"part 2: {part_two()}")


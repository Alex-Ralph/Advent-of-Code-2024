input = open("input-data/day09.txt").read().strip()
data = [int(x) for x in input]

def part_one():
    file_list = zip(range(len(data[::2])), data[::2])
    file_list = [[x[0]] * x[1] for x in file_list]
    sys_list = list(zip(file_list, ([None] * x for x in data[1::2])))
    sys_list = (y for x in sys_list for y in x) # flatten the list by one
    sys_files = [y for x in sys_list for y in x]
    sys_files += file_list[-1]

    while None in sys_files:
        defrag_block = sys_files.pop()
        if defrag_block is not None:
            sys_files[sys_files.index(None)] = defrag_block

    checksum = 0
    for index, x in enumerate(sys_files):
        checksum += x * index
    return checksum

def part_two():
    index = 0
    file_id = 0
    files = []
    spaces = []
    fileiter = iter(data[:-1])
    for file in fileiter:
        empty = next(fileiter)
        files.append([index, file_id, file]) # starting index, file id, file length
        index += file
        file_id += 1
        spaces.append([index, empty]) # starting index, length
        index += empty
    last = data[-1]
    files.append([index, file_id, last])
    files.reverse()
    checksum = 0
    for file in files:
        for space in spaces:
            if space[0] > file[0]:
                break
            if space[1] >= file[2]:
                file[0] = space[0]
                space[0] += file[2]
                space[1] -= file[2]
                if space[1] == 0:
                    spaces.remove(space)
                break
        for _ in range(file[2]):
            checksum += file[1] * file[0]
            file[0] += 1
    return checksum

print(f"Part one: {part_one()}")
print(f"Part two: {part_two()}")
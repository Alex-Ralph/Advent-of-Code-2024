import math
import functools

data = open("input-data/day11.txt").read()
stones = [int(x) for x in data.split()]

@functools.cache
def blink_at_stone(stone: int, generations: int):
    """Returns the number of stones you'd get if you blinked for n generations, from one starting stone"""
    if generations == 0:
        return 1
    if stone == 0:
        return blink_at_stone(1, generations-1)
    else:
        digits = int(math.log10(stone)+1)
        if digits % 2 == 1:
            return blink_at_stone(stone * 2024, generations - 1)
        else:
            new_stones = divmod(stone, pow(10, digits/2))
            return blink_at_stone(new_stones[0], generations-1) + blink_at_stone(new_stones[1], generations-1)

def count_rocks(cycles: int) -> int:
    """Returns rock count for 'cycles' generations"""
    return sum(blink_at_stone(x, cycles) for x in stones)

print(f"Part one: {count_rocks(25)}")
print(f"Part two: {count_rocks(75)}")
def parse_data():
    with open("test-data/day22.txt") as file:
        return [int(x) for x in file.read().split("\n")]

def mix(val, secret):
    return val ^ secret

def prune(secret):
    return secret % 16777216

def secret_generator(secret):
    while True:
        secret = prune(mix(secret * 64, secret))
        secret = prune(mix(int(secret / 32), secret))
        secret = prune(mix(secret * 2048, secret))
        yield secret

def part_one():
    secrets = parse_data()
    secret_sum = 0
    for secret in secrets:
        gen = secret_generator(secret)
        for _ in range(1999):
            next(gen)
        secret_sum += next(gen)
    print(secret_sum)

def part_two():
    """ The dumbest way of solving part 2:
    1. Create a dictionary for each secret, {pattern: value}
    2. For each possible pattern, sum up the total
    3. return the sum total for the best pattern
    """
    secrets = parse_data()
    secret_moves_and_prices = []
    for secret in secrets:
        secret_gen = secret_generator(secret)
        secret_list = [secret]
        secret_list += [next(secret_gen) for _ in range(1999)]
        price_list = [int(str(x)[-1]) for x in secret_list]
        price_moves = [(price_list[x-3] - price_list[x-4],
                        price_list[x-2] - price_list[x-3],
                        price_list[x-1] - price_list[x-2],
                        price_list[x] - price_list[x-1]) for x in range(4, 2000)]
        moves_and_prices = list(zip(price_moves, price_list[4:]))
        secret_moves_and_prices.append(moves_and_prices)
    possible_moves = [(a,b,c,d) for a in range(-9, 10) # this also contains many impossible moves
                      for b in range(-9, 10)
                      for c in range(-9, 10)
                      for d in range(-9, 10)]
    move_vals = []
    i = 0
    for move in possible_moves:
        move_val = 0
        for x in secret_moves_and_prices:
            for price_moves, price in x:
                if price_moves == move:
                    move_val += price
                    continue
        move_vals.append(move_val)
        i += 1
        print(i)
    print(max(move_vals))


# part_one()
part_two()
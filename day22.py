import line_profiler

def parse_data():
    with open("input-data/day22.txt") as file:
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

def get_price_changes(price_list: list[int]):
    return  [(price_list[x-3] - price_list[x-4],
            price_list[x-2] - price_list[x-3],
            price_list[x-1] - price_list[x-2],
            price_list[x] - price_list[x-1]) for x in range(4, len(price_list))]

def create_secret_dict(secret: int):
    gen = secret_generator(secret)
    secrets = [secret] + [next(gen) for _ in range(1999)]
    prices = [int(str(x)[-1]) for x in secrets]
    price_changes = get_price_changes(prices)
    relevant_prices = prices[4:]
    secret_dict = {}
    for id, changes in enumerate(price_changes):
        if changes not in secret_dict:
            secret_dict[changes] = relevant_prices[id]
    return secret_dict

@line_profiler.profile
def part_one():
    secrets = parse_data()
    secret_sum = 0
    for secret in secrets:
        gen = secret_generator(secret)
        for _ in range(1999):
            next(gen)
        secret_sum += next(gen)
    print(secret_sum)

@line_profiler.profile
def part_two():
    secrets = parse_data()
    secret_moves_and_prices = []
    for secret in secrets:
        secret_moves_and_prices.append(create_secret_dict(secret))
    possible_moves = [(a,b,c,d) for a in range(-9, 10) # this also contains many impossible moves
                      for b in range(-9, 10)
                      for c in range(-9, 10)
                      for d in range(-9, 10)]
    move_vals = []
    for move in possible_moves:
        move_price = 0
        for x in secret_moves_and_prices:
            if move in x:
                move_price += x[move]
        move_vals.append(move_price)
    print(max(move_vals))


part_one()
part_two()
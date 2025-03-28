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

def create_secret_list(secret: int) -> list[tuple[tuple[int], int]]:
    gen = secret_generator(secret)
    secrets = [secret] + [next(gen) for _ in range(1999)]
    prices = [int(str(x)[-1]) for x in secrets]
    price_changes = get_price_changes(prices)
    relevant_prices = prices[4:]
    secret_dict = {}
    for id, changes in enumerate(price_changes):
        if changes not in secret_dict:
            secret_dict[changes] = relevant_prices[id]
    return [(key, value) for key, value in secret_dict.items()]

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
    move_prices = {(a,b,c,d): 0 for a in range(-9, 10) # this also contains many impossible moves
                      for b in range(-9, 10)
                      for c in range(-9, 10)
                      for d in range(-9, 10)}
    for secret in secrets:
        secret_list = create_secret_list(secret)
        for x in secret_list:
            move_prices[x[0]] += x[1]
    print(max(move_prices.values()))



part_one()
part_two()
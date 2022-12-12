example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def _task(data, cost_func):
    positions = [int(i) for i in data.strip().split(",")]
    min_fuel = None
    for target in range(min(positions), max(positions) + 1):
        fuel = 0
        for position in positions:
            fuel += cost_func(position, target)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


def task1(data):
    return _task(data, lambda postition, target: abs(postition - target))


def task2(data):
    def f(position, target):
        n = int(abs(position - target))
        return (n**2 + n) // 2

    return _task(data, f)


print(f"{task1(example1)=}")
print(f"{task1(data)=}")

print(f"{task2(example1)=}")
print(f"{task2(data)=}")

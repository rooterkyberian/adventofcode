example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def task(data):
    x = depth = 0
    aim = 0
    for move, distance in (l.split() for l in data.splitlines()):
        distance = int(distance)
        match move:
            case "forward":
                x += distance
                depth += aim * distance
            case "up":
                aim -= distance
            case "down":
                aim += distance
    return x * depth


print(task(example1))
print(task(data))

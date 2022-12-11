example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def task1(data):
    x = depth = 0
    for move, distance in (l.split() for l in data.splitlines()):
        distance = int(distance)
        match move:
            case "forward":
                x += distance
            case "up":
                depth -= distance
            case "down":
                depth += distance
    return x * depth


print(task1(example1))
print(task1(data))

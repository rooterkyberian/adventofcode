example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def task2(data):
    rises = 0
    buf = []
    for depth in map(int, data.splitlines()):
        buf.append(depth)
        previous = buf[-4:-1]
        buf = buf[-3:]
        if len(previous) == 3 and sum(buf) > sum(previous):
            rises += 1
    return rises


print(task2(example1))
print(task2(data))

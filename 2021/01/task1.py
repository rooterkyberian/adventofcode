example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def count_rises(data):
    rises = 0
    previous_depth = None
    for depth in map(int, data.splitlines()):
        if previous_depth is not None and depth > previous_depth:
            rises += 1
        previous_depth = depth
    return rises


print(count_rises(example1))
print(count_rises(data))

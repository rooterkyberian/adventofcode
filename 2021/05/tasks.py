import itertools
import re
from pprint import pprint

import numpy as np

example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def read_lines(data):
    for line in data.splitlines():
        x1, y1, x2, y2 = (int(n) for n in re.findall(r"\d+", line))
        yield [(x1, y1), (x2, y2)]


def unending(x1, x2, n=0):
    d = -1 if x2 < x1 else 1
    return itertools.chain(
        range(x1, x2 + d, d),
        itertools.repeat(x2, n),
    )


def grow_array(arr, new_shape):
    if arr.shape == new_shape:
        return arr
    new_arr = np.zeros(new_shape, dtype=arr.dtype)
    new_arr[: arr.shape[0], : arr.shape[1]] = arr
    return new_arr


def calculate_overlaps(lines, all=False):
    overlaps = np.array([[]], dtype=int, order="F")
    for ((x1, y1), (x2, y2)) in lines:
        max_x = max(x1, x2, overlaps.shape[1] - 1)
        max_y = max(y1, y2, overlaps.shape[0] - 1)
        overlaps = grow_array(overlaps, (max_y + 1, max_x + 1))
        if all or x1 == x2 or y1 == y2:
            counts = abs(x1 - x2), abs(y1 - y2)
            n = int(abs(counts[0] - counts[1]))
            for (x, y) in zip(unending(x1, x2, n=n), unending(y1, y2, n=n)):
                overlaps[y][x] += 1
    return (overlaps > 1).sum()


def task1(data):
    lines = read_lines(data)
    return calculate_overlaps(lines)


def task2(data):
    lines = read_lines(data)
    return calculate_overlaps(lines, all=True)


print(f"{task1(example1)=}")
print(f"{task1(data)=}")

print(f"{task2(example1)=}")
print(f"{task2(data)=}")

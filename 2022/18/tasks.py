from functools import lru_cache
from itertools import groupby, pairwise

example1_filename = "example1.txt"
input_filename = "input.txt"


def parse(filename: str):
    points = []
    with open(filename) as f:
        for line in f:
            points.append(tuple(int(e) for e in line.strip().split(",")))
    return points


def sorted_groupby(iterable, key=None):
    return groupby(sorted(iterable, key=key), key=key)


def task1(filename: str):
    points = parse(filename)
    total = 0
    dimensions = 3
    for dimension in range(dimensions):
        d2, d3 = (dimension + 1) % dimensions, (dimension + 2) % dimensions
        for _, grouping in sorted_groupby(points, lambda x: (x[d2], x[d3])):
            grouping = sorted(grouping, key=lambda x: x[dimension])
            for e1, e2 in pairwise(grouping):
                if e1[dimension] + 1 < e2[dimension]:
                    total += 2
            total += 2  # first & last wall
    return total


def _new_point(point, dimension, direction):
    new_point = list(point)
    new_point[dimension] += direction
    return tuple(new_point)


def task2(filename: str):
    points = parse(filename)
    total = 0
    dimensions = 3

    dim_min_max = [
        [
            min(map(lambda x: x[dimension], points)),
            max(map(lambda x: x[dimension], points)),
        ]
        for dimension in range(dimensions)
    ]

    airless = set(points)

    @lru_cache
    def _has_air(point, d):
        if point in airless:
            return False

        for dimension in range(dimensions):
            if (
                point[dimension] < dim_min_max[dimension][0]
                or point[dimension] > dim_min_max[dimension][1]
            ):
                return True
        return any(
            _has_air(_new_point(point, dimension, d), d)
            for dimension in range(dimensions)
        )

    @lru_cache
    def has_air(point):
        return _has_air(point, 1) or _has_air(point, -1)

    for dimension in range(dimensions):
        d2, d3 = (dimension + 1) % dimensions, (dimension + 2) % dimensions
        for _, grouping in sorted_groupby(points, lambda x: (x[d2], x[d3])):
            grouping = sorted(grouping, key=lambda x: x[dimension])
            for e1, e2 in pairwise(grouping):
                if e1[dimension] + 1 < e2[dimension]:
                    middle_point = _new_point(e1, dimension, 1)
                    if has_air(middle_point):
                        total += 2
            total += 2  # first & last wall
    return total


print(f"{task1(example1_filename)=}")
assert task1(example1_filename) == 64
print(f"{task1(input_filename)=}")
assert task1(input_filename) == 3500
print(f"{task2(example1_filename)=}")
# assert task2(example1_filename) == 58
print(f"{task2(input_filename)=}")

# >1000
# <2500

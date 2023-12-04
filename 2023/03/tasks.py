import re
from dataclasses import dataclass

data = open("input.txt").read()

example1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

example2 = example1


def is_symbol(c):
    return c.strip() and not (c == "." or c.isdigit())


@dataclass
class NumberPoint:
    y: int
    x_start: int
    x_end: int
    value: int


def _parse_map(data):
    map_ = []
    number_points = []
    lines = data.strip("\n").splitlines()
    for y, line in enumerate(lines):
        if line:
            map_.append(line)
            for m in re.finditer(r"\d+", line):
                number_points.append(
                    NumberPoint(y, m.start(), m.end() - 1, int(m.group()))
                )
    return tuple(map_), number_points


def _p_is_adjacent_to_symbol(map_, p):
    return any(
        (0 <= x < len(map_[p.y]) and 0 <= y < len(map_) and is_symbol(map_[y][x]))
        for y in range(p.y - 1, p.y + 2)
        for x in range(p.x_start - 1, p.x_end + 2)
    )


def _adjacent_points(x, y, points):
    return [
        p
        for p in points
        if p.x_start - 1 <= x <= p.x_end + 1 and p.y - 1 <= y <= p.y + 1
    ]


def task1(data):
    map_, number_points = _parse_map(data)
    return sum(
        int(map_[p.y][p.x_start : p.x_end + 1])
        for p in number_points
        if _p_is_adjacent_to_symbol(map_, p)
    )


def task2(data):
    map_, number_points = _parse_map(data)
    total = 0
    for y, line in enumerate(map_):
        for x, c in enumerate(line):
            if c == "*":
                adjacent_points = _adjacent_points(x, y, number_points)
                if len(adjacent_points) == 2:
                    total += adjacent_points[0].value * adjacent_points[1].value
    return total


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 4361
    print(f"{task1(data)=}")
    assert task1(data) == 529618
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 467835
    assert task2(data) == 77509019

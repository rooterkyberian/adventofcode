from itertools import count

example1 = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
"""

example2 = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

data = open("input.txt").read()

from dataclasses import dataclass


@dataclass
class Blizzard:
    x: int
    y: int
    direction: tuple[int, int]


def read_data(data):
    blizzards = []
    for y, row in enumerate(data.strip().splitlines()):
        for x, c in enumerate(row):
            if c in "v^<>":
                blizzards.append(
                    Blizzard(
                        x, y, {"v": (0, 1), "^": (0, -1), "<": (-1, 0), ">": (1, 0)}[c]
                    )
                )
    return (x + 1, y + 1), blizzards


def print_phase(map_dims, blizzards, walls, r, pos=None):
    print(f"Round {r}")
    bliz_pos = {(b.x, b.y) for b in blizzards}
    for y in range(map_dims[1]):
        for x in range(map_dims[0]):
            if pos and (x, y) == pos:
                print("X", end="")
            elif (x, y) in walls:
                print("#", end="")
            elif (x, y) in bliz_pos:
                print("b", end="")
            else:
                print(".", end="")
        print()
    print()


@dataclass(slots=True)
class Path:
    moves: list[tuple[int, int]]
    reached_goals: int


def task1(data, v=0):
    return _task(
        data,
        [
            (-2, -1),
        ],
        v,
    )


def task2(data, v=0):
    return _task(
        data,
        [
            (-2, -1),
            (1, 0),
            (-2, -1),
        ],
        v,
    )


def _task(data, goals, v):
    map_dims, blizzards = read_data(data)
    goals = [(g[0] % map_dims[0], g[1] % map_dims[1]) for g in goals]
    r = None
    stack = [Path([(1, 0)], 0)]

    walls = (
        {(0, y) for y in range(map_dims[1])}
        | {(map_dims[0] - 1, y) for y in range(map_dims[1])}
        | {(x, 0) for x in range(map_dims[0]) if x != 1}
        | {(x, map_dims[1] - 1) for x in range(map_dims[0]) if x != map_dims[0] - 2}
    )

    for r in count(1):
        if v > 1:
            print_phase(map_dims, blizzards, walls, r)
        for b in blizzards:
            b.x += b.direction[0]
            b.y += b.direction[1]
            if b.x == 0:
                b.x = map_dims[0] - 2
            elif b.x == map_dims[0] - 1:
                b.x = 1
            elif b.y == 0:
                b.y = map_dims[1] - 2
            elif b.y == map_dims[1] - 1:
                b.y = 1
        hazards = {(b.x, b.y) for b in blizzards}
        new_stack = []
        already_proposed = set()
        for path in stack:
            last_pos = path.moves[-1]
            for xd, yd in (
                (0, 0),
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
            ):
                goals_reached = path.reached_goals
                new_pos = last_pos[0] + xd, last_pos[1] + yd
                # print(goals, goals[goals_reached], new_pos)
                if goals[goals_reached] == new_pos:
                    goals_reached += 1
                    if goals_reached == len(goals):
                        if v:
                            print(f"Found {path.moves} path in {r} rounds")
                        return len(path.moves)
                if (
                    new_pos in already_proposed
                    or new_pos[0] < 0
                    or new_pos[1] < 0
                    or new_pos[0] >= map_dims[0]
                    or new_pos[1] >= map_dims[1]
                    or new_pos in walls
                    or new_pos in hazards
                ):
                    if new_pos not in already_proposed:
                        already_proposed.add(new_pos)
                    continue
                already_proposed.add(new_pos)
                new_stack.append(Path(path.moves + [new_pos], goals_reached))

        max_goals = max(p.reached_goals for p in new_stack)
        stack = [path for path in new_stack if path.reached_goals == max_goals]
    return r


print(f"{task1(example2, 2)=}")
assert task1(example2) == 18
print(f"{task1(data)=}")
assert task1(data) == 251
print(f"{task2(example2)=}")
assert task2(example2) == 54
print(f"{task2(data)=}")

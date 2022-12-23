from collections import defaultdict
from itertools import count, product

example1 = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
example2 = """
.....
..##.
..#..
.....
..##.
.....
"""

data = open("input.txt").read()

from dataclasses import dataclass


@dataclass
class Elf:
    x: int
    y: int
    proposal: tuple = None


def read_data(data):
    for y, row in enumerate(data.strip().splitlines()):
        for x, c in enumerate(row):
            if c == "#":
                yield x, y


def proposal(
    elf_positions: set[tuple[int, int]], elf: Elf, direction_offset: int = 0
) -> tuple[int, int] | None:
    """


    If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.


    :param elf_positions:
    :param elf:
    :return:
    """
    if not any(
        (elf.x + dx, elf.y + dy) in elf_positions
        for dx, dy in product(range(-1, 2), repeat=2)
        if dx != 0 or dy != 0
    ):
        return None

    for d in range(direction_offset, direction_offset + 4):
        d %= 4
        if d == 0 and all(
            (elf.x + i, elf.y - 1) not in elf_positions for i in range(-1, 2)
        ):
            return elf.x, elf.y - 1
        elif d == 1 and all(
            (elf.x + i, elf.y + 1) not in elf_positions for i in range(-1, 2)
        ):
            return elf.x, elf.y + 1
        elif d == 2 and all(
            (elf.x - 1, elf.y + i) not in elf_positions for i in range(-1, 2)
        ):
            return elf.x - 1, elf.y
        elif d == 3 and all(
            (elf.x + 1, elf.y + i) not in elf_positions for i in range(-1, 2)
        ):
            return elf.x + 1, elf.y
    return None


def _task(data, v=0, rounds=None):
    elves = [Elf(*pos) for pos in read_data(data)]
    counter = count() if rounds is None else range(rounds)
    r = -1
    for r in counter:
        positions = {(e.x, e.y) for e in elves}
        proposals = defaultdict(int)
        for e in elves:
            e.proposal = proposal(positions, e, r)
            proposals[e.proposal] += 1
        for e in elves:
            if e.proposal and proposals[e.proposal] == 1:
                e.x, e.y = e.proposal
            else:
                e.proposal = None

        if v > 1:
            positions = {(e.x, e.y) for e in elves}
            print(f"Round {r+1}")
            for y in range(min(e.y for e in elves), max(e.y for e in elves) + 1):
                for x in range(min(e.x for e in elves), max(e.x for e in elves) + 1):
                    if (x, y) in positions:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()

        if all(e.proposal is None for e in elves):
            break

    area = (max(e.x for e in elves) - min(e.x for e in elves) + 1) * (
        max(e.y for e in elves) - min(e.y for e in elves) + 1
    )
    return r + 1, area - len({(e.x, e.y) for e in elves})


def task1(*args, **kwargs):
    return _task(*args, **kwargs, rounds=10)[1]


def task2(data):
    return _task(data, rounds=None)[0]


print(f"{task1(example2, v=2)=}")
print(f"{task1(example1, v=2)=}")
print(f"{task1(data)=}")
print(f"{task2(example1)=}")
print(f"{task2(data)=}")

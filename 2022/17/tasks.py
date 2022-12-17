from __future__ import annotations

import itertools
from functools import lru_cache

from tqdm import tqdm

example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()

shapes_data = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split(
    "\n\n"
)


def rocks_gen():
    for rock in itertools.cycle(shapes_data):
        yield rock.split("\n")


def moves_gen(data):
    yield from itertools.cycle(data.strip())


def rock_data(rock_shape, ledge_edge, w):
    rock_ = []
    for line in rock_shape.splitlines():
        rock_.append("." * ledge_edge + line + "." * (w - ledge_edge - len(line)))
    return tuple(rock_)


@lru_cache
def _cannot_trans(rock, move):
    if move == "<":
        return any(line[0] == "#" for line in rock)
    else:
        return any(line[-1] == "#" for line in rock)


@lru_cache
def _trans_rock(rock, d):
    if d == "<":
        return tuple(f"{line[1:]}." for line in rock)
    else:
        return tuple(f".{line[:-1]}" for line in rock)


def trans_rock(
    rock: tuple[str], d: str, tower: list[str] | None = None, y: int = 0
) -> tuple[str]:
    if _cannot_trans(rock, d):
        return rock
    new_rock = _trans_rock(rock, d)
    if tower is not None and collision(new_rock, tower, y):
        return rock
    return tuple(new_rock)


@lru_cache
def _line_collision(line1, line2):
    return any(x == "#" and x2 == "#" for x, x2 in zip(line1, line2))


def collision(rock, tower, y):
    if len(tower) < y + len(rock):
        return True
    for r_y in range(len(rock) - 1, -1, -1):
        line = rock[r_y]
        t_y = y + r_y
        tower_line = tower[t_y]
        if _line_collision(line, tower_line):
            return True
    return False


@lru_cache
def _line_collide(line1, line2):
    return "".join("#" if "#" in (x, x2) else "." for x, x2 in zip(line1, line2))


def collide(rock, tower, y):
    for r_y, line in enumerate(rock):
        t_y = y + r_y
        tower_line = tower[t_y]
        tower[t_y] = _line_collide(line, tower_line)


def task1(data, i=2022, verbose=False):
    wide = 7
    empty_space = 3
    rocks = itertools.cycle(
        tuple(rock_data(r, ledge_edge=2, w=wide) for r in shapes_data)
    )
    moves = itertools.cycle(enumerate(data.strip()))
    tower = []
    t_h = 0
    true_t_h = 0

    def true_h():
        return t_h + true_t_h

    move_cache = {}
    _total_rocks = 0
    rocks_thingy = (x for x in tqdm(zip(range(i), rocks), total=i))

    def total_rocks(c):
        return _total_rocks + c

    for rock_counter, rock in rocks_thingy:
        if total_rocks(rock_counter) + 1 > i:
            break
        tower[:0] = ["." * wide] * (empty_space + len(rock))

        # print(f"Tower in progress ({t_h=}): ", "\n".join(tower), sep="\n")
        for y, (move_id, move) in enumerate(moves):
            if t_h and not move_cache.get("used"):
                last_idx = len(tower) - t_h
                last_line = tuple(
                    tower[last_idx : last_idx + 300]
                )  # another naive buffer
                current_stage = (last_line, rock, move_id)
                if current_stage in move_cache:
                    move_cache["used"] = True
                    print("Cache hit!")
                    rocks_passed, prev_t_h = move_cache.get(current_stage)
                    print(f"{move_cache.get(current_stage)=}")
                    rocks_passed = total_rocks(rock_counter) - rocks_passed
                    times = (i - rock_counter) // rocks_passed
                    print(f"{times=} {rocks_passed=} {rock_counter=} {i=}")
                    print(f"{rocks_passed=} {times=} {y=}")
                    true_t_h += (true_h() - prev_t_h) * times
                    _total_rocks += rocks_passed * times
                    if total_rocks(rock_counter) >= i:
                        break
                else:
                    move_cache[current_stage] = total_rocks(rock_counter), true_h()

            can_collide = y >= empty_space
            rock = trans_rock(rock, move, tower if can_collide else None, y)
            if can_collide and collision(rock, tower, y + 1):
                collide(rock, tower, y)
                t_h = max(t_h, len(tower) - y)
                tower = tower[-t_h:]
                cutoff = 100  # naive solution assuming there will be full line there somewhere
                if t_h > cutoff * 10:
                    t_h -= cutoff
                    true_t_h += cutoff
                    del tower[-cutoff:]
                break

    if verbose:
        print("Tower")
        for line in tower:
            print(line)
    return true_h()


def task2(data):
    return task1(data, i=1000000000000)


print(f"{task1(example1, verbose=True, i=100)=}")
print(f"{task1(example1)=}")
assert task1(example1) == 3068
print(f"{task1(data)=}")
assert task1(data) == 3144
print(f"{task2(example1)=}")
assert task2(example1) == 1514285714288
print(f"{task2(data)=}")

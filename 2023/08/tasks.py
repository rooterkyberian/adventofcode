# ruff: noqa: F841

import dataclasses
import functools
import itertools
import re

data = open("input.txt").read()

example1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

example3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


@dataclasses.dataclass
class Node:
    L: str
    R: str


def parse(data: str):
    steps, node_desc = data.strip().split("\n\n", maxsplit=1)
    nodes = {}
    for node_match in re.findall(r"(\w+) = \((\w+), (\w+)\)", node_desc):
        nodes[node_match[0]] = Node(*node_match[1:])
    return steps, nodes


def task1(data):
    steps, nodes = parse(data)
    current_node_name = "AAA"
    for counter, step in enumerate(itertools.cycle(steps)):
        if current_node_name == "ZZZ":
            return counter
        current_node_name = getattr(nodes[current_node_name], step)


@functools.cache
def task2(data):
    """

    I expect the "right" solution to use LCM, but that requires thinking ;p
    So here is the brute force solution (takes couple minutes to solve the puzzle)
    """
    steps, nodes = parse(data)
    all_start_nodes = [
        node_name for node_name, node in nodes.items() if node_name.endswith("A")
    ]

    @functools.cache
    def next_z(start_node_name: str, steps_offset: int):
        current_node_name = start_node_name
        for counter, step in enumerate(
            itertools.cycle(steps[steps_offset:] + steps[:steps_offset]), start=1
        ):
            current_node_name = getattr(nodes[current_node_name], step)
            if current_node_name.endswith("Z"):
                return current_node_name, counter

    ghosts = {node_name: 0 for node_name in all_start_nodes}
    ghosts_current_node = {node_name: node_name for node_name in all_start_nodes}
    ghost_count = len(ghosts)
    while True:
        max_offset = max(ghosts.values()) or 1
        same_counter = 0
        for node_name, offset in list(ghosts.items()):
            if offset < max_offset:
                ghosts_current_node[node_name], offset_inc = next_z(
                    ghosts_current_node[node_name], offset % len(steps)
                )
                ghosts[node_name] += offset_inc
            else:
                same_counter += 1
        if same_counter == ghost_count:
            return list(ghosts.values())[0]


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 2
    assert task1(example2) == 6
    print(f"{task1(data)=}")
    assert task1(data) == 13771
    print(f"{task2(example2)=}")
    print(f"{task2(example3)=}")
    assert task2(example2) == 6
    assert task2(example3) == 6
    print(f"{task2(data)=}")
    assert task2(data) == 13129439557681

import json
import operator
import re
from functools import reduce

import pytest

example1_filename = "example1.txt"
input_filename = "input.txt"


def read_blueprints(filename):
    with open(filename) as f:
        data = f.read()
    robot_re = re.compile(
        r"Each (?P<robot>\w+) robot costs (?P<cost>\d+ \w+( and \d+ \w+)?)"
    )
    for bid, b_line in enumerate(data.strip().split("Blueprint")):
        if b_line := b_line.strip():
            blueprint = {}
            for r_line in b_line.split("."):
                if not (r_line := r_line.strip()):
                    continue
                m = robot_re.search(r_line)
                robot_type = m.group("robot")
                blueprint[robot_type] = {}

                for required in m.group("cost").split("and"):
                    amount, resource = required.split()
                    blueprint[robot_type][resource] = int(amount)

            yield bid, blueprint


def blueprint_quality(bid, geode):
    return bid * geode


def deepcopy(d):
    return json.loads(json.dumps(d))


def update_resources(world, minutes):
    new_world = {"robots": world["robots"], "resources": dict(world["resources"])}
    for robot_type, robot_count in world["robots"].items():
        new_world["resources"][robot_type] += robot_count * minutes
    return new_world


def _task1_alternatives(world, blueprint, minutes, blueprint_info):
    # print(f"{minutes=} {world=} {blueprint_info=}")
    worst_case_geode = world["robots"]["geode"] * minutes + world["resources"]["geode"]
    if worst_case_geode > blueprint_info["best_geode"]:
        blueprint_info["best_geode"] = worst_case_geode
        print(f"{worst_case_geode=} {minutes=} {world=}")
    else:
        n = minutes - 1
        best_geode_growth = n * (n + 1) / 2
        geode_hope = worst_case_geode + best_geode_growth
        # print(f"{worst_case_geode=} {best_geode_growth=} {geode_hope=}")
        if geode_hope <= blueprint_info["best_geode"]:
            return
    yield worst_case_geode
    if minutes <= 1:
        return  # no more time to build geode robots
    new_world = update_resources(world, 1)
    minutes -= 1
    for robot_type in blueprint_info["priority"]:
        if robot_type == "geode":
            is_needed = True
        else:
            is_needed = (
                minutes > 1
                and world["robots"][robot_type] < blueprint_info["max_cost"][robot_type]
            )
            is_needed = (
                is_needed
                and any(  # is it needed for production of robots of resource with higher priority?
                    blueprint[other_resource].get(robot_type, 0)
                    > world["robots"][robot_type]
                    for other_resource in blueprint_info["priority"][
                        : blueprint_info["priority"].index(robot_type)
                    ]
                )
            )
        if is_needed and all(
            world["resources"][resource] >= cost
            for resource, cost in blueprint[robot_type].items()
        ):
            new_world_with_robot = deepcopy(new_world)
            for resource, cost in blueprint[robot_type].items():
                new_world_with_robot["resources"][resource] -= cost
            new_world_with_robot["robots"][robot_type] += 1
            yield from _task1_alternatives(
                new_world_with_robot, blueprint, minutes, blueprint_info
            )
    yield from _task1_alternatives(new_world, blueprint, minutes, blueprint_info)


def task1_blueprint_score(blueprint, minutes=24):
    world = {
        "robots": {
            type_: (1 if type_ == "ore" else 0) for type_ in reversed(blueprint)
        },
        "resources": {type_: 0 for type_ in blueprint},
    }
    blueprint_info = {
        "best_geode": 0,
        "max_cost": {
            type_: max(costs.get(type_, 0) for costs in blueprint.values())
            for type_ in blueprint
        },
        "priority": ["geode", "obsidian", "clay", "ore"],
    }
    return max(_task1_alternatives(world, blueprint, minutes, blueprint_info))


def task1(filename):
    qualities = []
    for bid, blueprint in read_blueprints(filename):
        score = task1_blueprint_score(blueprint)
        print(f"Blueprint {bid} {score=}")
        qualities.append(blueprint_quality(bid, score))
    return sum(qualities)


def task2(filename):
    scores = []
    for bid, blueprint in list(read_blueprints(filename))[:3]:
        score = task1_blueprint_score(blueprint, 32)
        print(f"Blueprint {bid} {score=}")
        scores.append(score)
    print(f"Task 2 {filename=} {scores=}")
    return reduce(operator.mul, scores, 1)


@pytest.mark.skip
@pytest.mark.parametrize(
    "bid,expected",
    [
        (1, 9),
        (2, 12),
    ],
)
def test_task1_blueprint_score(bid, expected):
    blueprint = next(
        blueprint
        for bid_, blueprint in read_blueprints(example1_filename)
        if bid_ == bid
    )
    assert task1_blueprint_score(blueprint) == expected


@pytest.mark.skip
@pytest.mark.parametrize(
    "filename,expected",
    [
        (example1_filename, 33),
        (input_filename, 1150),  # >1128 , < 1200
    ],
)
def test_task1(filename, expected):
    assert task1(filename) == expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        (example1_filename, 56 * 62),
        (input_filename, 37367),
    ],
)
def test_task2(filename, expected):
    assert task2(filename) == expected

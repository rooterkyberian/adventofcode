import re
from functools import reduce

data = open("input.txt").read()

example1 = """
Time:      7  15   30
Distance:  9  40  200
"""

example2 = example1


def _parse_races_data(data):
    parsed = re.match(r"Time:([\s\d]+)\nDistance:([\s\d]+)", data.strip(), re.MULTILINE)
    times = list(map(int, parsed.group(1).split()))
    distances = list(map(int, parsed.group(2).split()))
    return times, distances


def _race_variants(race_time):
    for btn_press_len in range(1, race_time):
        distance = (race_time - btn_press_len) * btn_press_len
        yield btn_press_len, distance


def _ways_to_win(times, distances):
    ways_to_win = []
    for race_time, record_distance in zip(times, distances):
        ways_to_win.append(
            sum(record_distance < distance for _, distance in _race_variants(race_time))
        )

    return reduce(lambda a, b: a * b, ways_to_win, 1)


def task1(data):
    times, distances = _parse_races_data(data)
    return _ways_to_win(times, distances)


def task2(data):
    times, distances = _parse_races_data(data)
    times = [int("".join(str(t) for t in times))]
    distances = [int("".join(str(d) for d in distances))]
    return _ways_to_win(times, distances)


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 288
    print(f"{task1(data)=}")
    assert task1(data) == 633080
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 71503
    assert task2(data) == 20048741

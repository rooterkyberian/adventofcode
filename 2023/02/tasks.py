import re
from functools import reduce

data = open("input.txt").read()

example1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

example2 = example1

task1_config = {"red": 12, "green": 13, "blue": 14}


def _parse_games(data):
    games = {}
    for line in data.splitlines():
        if game_match := re.match(r"Game (\d+): (.*)", line):
            game_idx = int(game_match.group(1))
            games[game_idx] = []
            for elf_draw in game_match.group(2).split(";"):
                games[game_idx].append(
                    {
                        color: int(count)
                        for count, color in re.findall(r"(\d+) (\w+)", elf_draw)
                    }
                )
    return games


def task1(data):
    games = _parse_games(data)
    return sum(
        game_idx
        for game_idx, game in games.items()
        if all(
            all(
                count <= task1_config.get(color, 0) for color, count in elf_draw.items()
            )
            for elf_draw in game
        )
    )


def _min_config_for_game(game):
    config = {}
    for elf_draw in game:
        for color, count in elf_draw.items():
            config[color] = max(config.get(color, 0), count)
    return config


def _config_power(config):
    return reduce(lambda x, y: x * y, config.values(), 1)


def task2(data):
    games = _parse_games(data)

    return sum(_config_power(_min_config_for_game(game)) for game in games.values())


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 8
    print(f"{task1(data)=}")
    assert task1(data) == 2810
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 2286
    assert task2(data) == 69110

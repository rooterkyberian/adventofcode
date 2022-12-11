import json
from datetime import date

import requests

from pathlib import Path


def fetch_input(year, day, session):
    input_path = Path(f"{year}/{day:02d}/input.txt")
    if not input_path.exists():
        input_path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        resp = requests.get(url, cookies={"session": session})
        resp.raise_for_status()
        with input_path.open("wb") as f:
            f.write(resp.content)
    return input_path


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, default=date.today().year, nargs="?")
    args = parser.parse_args()
    with open(".adventofcode.json") as f:
        session = json.load(f)["session"]

    for day in range(1, 26):
        fetch_input(args.year, day, session).read_text()


if __name__ == "__main__":
    main()

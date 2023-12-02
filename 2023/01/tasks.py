import re

data = open("input.txt").read()

example1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def task1(data):
    return sum(
        int(numbers[0] + numbers[-1])
        for line in data.splitlines()
        if (numbers := re.findall(r"\d", line))
    )


number_literals = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def task2(data):
    def trans(x):
        return str(number_literals.get(x, x))

    return sum(
        (int(trans(numbers[0]) + trans(numbers[-1])))
        for line in data.splitlines()
        if (
            numbers := [
                m.group(1)
                for m in re.finditer(
                    "(?=(" + "|".join([r"\d", *number_literals]) + "))", line
                )
            ]
        )
    )


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 142
    print(f"{task1(data)=}")
    assert task1(data) == 54388
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 281
    # 51425 is wrong
    assert task2(data) == 53515

from collections import defaultdict

example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def task1(data, n=80):
    school = [int(x) for x in data.strip().split(",")]
    for _ in range(n):
        new_school = []
        for fish in school:
            fish -= 1
            if fish < 0:
                new_school.extend((6, 8))
            else:
                new_school.append(fish)
        school = new_school
    return len(school)


def task2(data):
    school = defaultdict(int)
    for fish in data.strip().split(","):
        school[int(fish)] += 1
    for _ in range(256):
        new_school = defaultdict(int)
        for fish_timer, count in school.items():
            fish_timer -= 1
            if fish_timer < 0:
                new_school[6] += count
                new_school[8] += count
            else:
                new_school[fish_timer] += count
        school = new_school
    return sum(school.values())


print(f"{task1(example1)=}")
print(f"{task1(data)=}")

print(f"{task2(example1)=}")
print(f"{task2(data)=}")

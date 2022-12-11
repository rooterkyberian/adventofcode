example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def task(data):
    report = list(data.splitlines())
    gamma = ""
    epsilon = ""
    for i in range(len(report[0])):
        zeros = sum(l[i] == "0" for l in report) / len(report)
        gamma += "0" if zeros > 0.5 else "1"
        epsilon += "1" if zeros > 0.5 else "0"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


print(task(example1))
print(task(data))

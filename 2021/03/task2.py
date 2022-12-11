example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def zero_bit_ratio(report, bit):
    return sum(l[bit] == "0" for l in report) / len(report)


def o2_bitcriteria(zero_ratio):
    if zero_ratio > 0.5:
        return "0"
    elif zero_ratio < 0.5:
        return "1"
    else:
        return "1"


def co2_bitcriteria(zero_ratio):
    if zero_ratio > 0.5:
        return "1"
    elif zero_ratio < 0.5:
        return "0"
    else:
        return "0"


def searcher(report, bitcriteria):
    while True:
        for i in range(len(report[0])):
            if len(report) == 1:
                return report[0]
            zero_ratio = zero_bit_ratio(report, i)
            bit = bitcriteria(zero_ratio)
            report = [l for l in report if l[i] == bit]


def task(data):
    report = list(data.splitlines())
    o2 = int(searcher(report, o2_bitcriteria), 2)
    co2 = int(searcher(report, co2_bitcriteria), 2)
    return o2 * co2


print(task(example1))
print(task(data))

example1 = open("example1.txt").read().strip()
data = open("input.txt").read().strip()


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def check_board(board: list[list[int]], visited: set[int]):
    for row in board:
        if all(e in visited for e in row):
            return True
    for row in transpose(board):
        if all(e in visited for e in row):
            return True
    return False


def read_data(data):
    boards = []
    header, *lines = data.splitlines()
    numbers = [int(n) for n in header.split(",")]
    for line in lines:
        if line:
            if not boards or len(boards[-1]) == 5:
                boards.append([])
            boards[-1].append([int(n) for n in line.split()])
    return numbers, boards


def winner_score(data):
    numbers, boards = read_data(data)
    visited = set()
    for number in numbers:
        visited.add(number)
        for board in list(boards):
            if check_board(board, visited):
                yield (
                    sum(sum(i for i in row if i not in visited) for row in board)
                    * number
                )
                boards.remove(board)


def task1(data):
    return next(winner_score(data))


def task2(data):
    for score in winner_score(data):
        pass
    return score


print(f"{task1(example1)=}")
print(f"{task1(data)=}")

print(f"{task2(example1)=}")
print(f"{task2(data)=}")

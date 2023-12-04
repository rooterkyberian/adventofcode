import re
from dataclasses import dataclass

data = open("input.txt").read()

example1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

example2 = example1


@dataclass
class Card:
    no: int
    winning: set
    numbers: set


def _parse_cards(data):
    cards = []
    for card_match in re.finditer(r"Card\s+(\d+): ([\d ]+) \| ([\d ]+)", data):
        card_no = int(card_match.group(1))
        winning = set(map(int, card_match.group(2).split()))
        numbers = set(map(int, card_match.group(3).split()))
        cards.append(Card(card_no, winning, numbers))
    return cards


def _card_value(card) -> int:
    won_numbers = card.winning & card.numbers
    return 2 ** (len(won_numbers) - 1) if won_numbers else 0


def task1(data):
    cards = _parse_cards(data)
    return sum(_card_value(card) for card in cards)


def task2(data):
    cards = _parse_cards(data)
    card_counters = [1] * len(cards)
    for card_no in range(len(card_counters)):
        card = cards[card_no]
        card_count = card_counters[card_no]
        won_numbers = card.winning & card.numbers
        for i in range(card_no + 1, min(card_no + 1 + len(won_numbers), len(cards))):
            card_counters[i] += card_count
    return sum(card_counters)


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 13
    print(f"{task1(data)=}")
    assert task1(data) == 27845
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 467835
    assert task2(data) == 77509019

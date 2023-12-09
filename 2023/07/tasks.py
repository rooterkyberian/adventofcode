# ruff: noqa: F841

import collections

data = open("input.txt").read()

example1 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

example2 = example1

CARDS = list(reversed("A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")))
CARDS_W_JOKER = list(reversed("A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")))


def _get_hand_value(hand: str):
    counter = collections.Counter(hand)
    hand_indexes = tuple(CARDS.index(card) for card in hand)
    match counter.most_common():
        case [(card, 5)]:
            return 7, hand_indexes
        case [(card, 4), *rest]:
            return 6, hand_indexes
        case [(card, 3), (card2, 2)]:
            return 5, hand_indexes
        case [(card, 3), *rest]:
            return 4, hand_indexes
        case [(card, 2), (card2, 2), *rest]:
            return 3, hand_indexes
        case [(card, 2), *rest]:
            return 1, hand_indexes
    return 0, hand_indexes


def _get_hand_value_with_joker(hand: str):
    counter = collections.Counter(hand)
    hand_indexes = tuple(CARDS_W_JOKER.index(card) for card in hand)
    match counter.most_common():
        case [(card, 5)]:
            return 7, hand_indexes
        case [(card, 4), *rest]:
            if "J" in hand:
                return 7, hand_indexes
            return 6, hand_indexes
        case [(card, 3), (card2, 2)]:
            if "J" in hand:
                return 7, hand_indexes
            return 5, hand_indexes
        case [(card, 3), *rest]:
            if "J" in hand:
                return 6, hand_indexes
            return 4, hand_indexes
        case [(card, 2), (card2, 2), *rest]:
            match hand.count("J"):
                case 0:
                    return 3, hand_indexes
                case 1:
                    return 5, hand_indexes
                case 2:
                    return 6, hand_indexes
        case [(card, 2), *rest]:
            match hand.count("J"):
                case 0:
                    return 1, hand_indexes
                case 1:
                    return 4, hand_indexes
                case 2:
                    return 4, hand_indexes
    return int("J" in hand), hand_indexes


def _parse_hands_bids(data: str):
    for line in data.strip().splitlines():
        hand, bid = line.strip().split()
        yield hand, int(bid)


def task1(data):
    hands_bids = _parse_hands_bids(data)
    return sum(
        rank * bid
        for rank, (_, bid) in enumerate(
            sorted(hands_bids, key=lambda x: _get_hand_value(x[0])), start=1
        )
    )


def task2(data):
    hands_bids = _parse_hands_bids(data)
    return sum(
        rank * bid
        for rank, (_, bid) in enumerate(
            sorted(hands_bids, key=lambda x: _get_hand_value_with_joker(x[0])), start=1
        )
    )


if __name__ == "__main__":
    print(f"{task1(example1)=}")
    assert task1(example1) == 6440
    print(f"{task1(data)=}")
    assert task1(data) == 247961593
    print(f"{task2(example2)=}")
    print(f"{task2(data)=}")
    assert task2(example2) == 5905
    assert task2(data) == 248750699

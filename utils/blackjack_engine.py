import random

SUITS = ["clubs", "diamonds", "hearts", "spades"]

RANKS = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K"
]


def create_deck():

    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append(
                f"{rank}_{suit}"
            )

    random.shuffle(deck)

    return deck


def draw_card(deck):

    return deck.pop()


def card_value(card):

    rank = card.split("_")[0]

    if rank in ["J", "Q", "K"]:
        return 10

    if rank == "A":
        return 11

    return int(rank)


def hand_value(hand):

    total = 0
    aces = 0

    for card in hand:

        value = card_value(card)

        total += value

        if value == 11:
            aces += 1

    while total > 21 and aces > 0:

        total -= 10
        aces -= 1

    return total


def is_blackjack(hand):

    return len(hand) == 2 and hand_value(hand) == 21


def dealer_play(deck, dealer_hand):

    while hand_value(dealer_hand) < 17:

        dealer_hand.append(
            draw_card(deck)
        )

    return dealer_hand


def compare(player, dealer):

    p = hand_value(player)
    d = hand_value(dealer)

    if p > 21:
        return "lose"

    if d > 21:
        return "win"

    if p > d:
        return "win"

    if p < d:
        return "lose"

    return "push"

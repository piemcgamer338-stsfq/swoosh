import random


SUITS = [
    "♠",
    "♥",
    "♦",
    "♣"
]


VALUES = [
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

        for value in VALUES:

            deck.append(
                {
                    "value": value,
                    "suit": suit
                }
            )


    return deck



def shuffle_deck(deck):

    random.shuffle(deck)

    return deck



def draw_card(deck):

    if len(deck) == 0:

        deck = create_deck()

        shuffle_deck(deck)


    return deck.pop()



def card_text(card):

    return (
        f"{card['value']}"
        f"{card['suit']}"
    )



def card_value(card):

    value = card["value"]


    if value in ["J", "Q", "K"]:

        return 10


    if value == "A":

        return 11


    return int(value)



def calculate_hand(cards):

    total = 0
    aces = 0


    for card in cards:

        total += card_value(card)


        if card["value"] == "A":

            aces += 1



    while total > 21 and aces:

        total -= 10

        aces -= 1


    return total



def is_blackjack(cards):

    return (
        len(cards) == 2
        and calculate_hand(cards) == 21
    )



def format_hand(cards):

    return " ".join(
        [
            card_text(card)
            for card in cards
        ]
    )

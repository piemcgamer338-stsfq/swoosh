import random


CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}


SUITS = [
    "spades",
    "hearts",
    "diamonds",
    "clubs"
]


class Card:

    def __init__(self, rank, suit):

        self.rank = rank
        self.suit = suit

        self.value = CARD_VALUES[rank]



    @property
    def filename(self):

        return (
            f"{self.rank}_of_{self.suit}.png"
        )



    @property
    def display(self):

        symbols = {
            "spades": "♠",
            "hearts": "♥",
            "diamonds": "♦",
            "clubs": "♣"
        }

        return (
            f"{self.rank}{symbols[self.suit]}"
        )




class HiLoDeck:

    def __init__(self):

        self.cards = []

        for suit in SUITS:

            for rank in CARD_VALUES:

                self.cards.append(
                    Card(
                        rank,
                        suit
                    )
                )

        random.shuffle(
            self.cards
        )



    def draw(self):

        if not self.cards:

            self.__init__()

        return self.cards.pop()




MULTIPLIERS = [
    1.00,
    1.50,
    2.00,
    2.50,
    3.00,
    3.50,
    4.00,
    4.50,
    5.00,
    5.50,
    6.00,
    6.50,
    7.00,
    7.50,
    8.00,
    8.50,
    9.00,
    9.50,
    10.00
]



def get_multiplier(
    streak
):

    if streak >= len(MULTIPLIERS):

        return MULTIPLIERS[-1]

    return MULTIPLIERS[
        streak
    ]




def compare_cards(
    previous,
    current,
    guess
):

    if current.value == previous.value:

        return "tie"


    if guess == "higher":

        if current.value > previous.value:

            return "win"

        return "lose"


    if current.value < previous.value:

        return "win"

    return "lose"

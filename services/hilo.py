from utils.hilo import (
    HiLoDeck,
    compare_cards,
    get_multiplier
)


class HiLoGame:

    def __init__(
        self,
        user_id,
        bet
    ):

        self.user_id = user_id
        self.bet = bet

        self.deck = HiLoDeck()

        self.current = self.deck.draw()

        self.previous = None

        self.streak = 0

        self.finished = False



    @property
    def multiplier(self):

        return get_multiplier(
            self.streak
        )



    @property
    def payout(self):

        return round(
            self.bet * self.multiplier,
            2
        )



    def guess(
        self,
        direction
    ):

        if self.finished:

            return (
                "finished",
                self.current
            )


        self.previous = self.current

        self.current = self.deck.draw()


        result = compare_cards(
            self.previous,
            self.current,
            direction
        )


        if result == "tie":

            return (
                "tie",
                self.current
            )


        if result == "win":

            self.streak += 1

            return (
                "win",
                self.current
            )


        self.finished = True

        return (
            "lose",
            self.current
        )



    def cashout(self):

        self.finished = True

        return self.payout

RATE = 0.01


async def add_rakeback(
    user,
    wager
):

    user.rakeback += wager * RATE


async def claim_rakeback(user):

    rb = user.rakeback

    user.balance += rb

    user.rakeback = 0

    return rb

RATE = 0.005


async def calculate_weekly(user):

    cashback = (
        user.weekly_wager * RATE
    )

    return cashback


async def claim_weekly(user):

    amount = await calculate_weekly(user)

    user.balance += amount

    user.weekly_wager = 0

    return amount

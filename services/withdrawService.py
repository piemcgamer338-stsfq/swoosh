from utils.constants import MIN_WITHDRAW_USD


async def can_withdraw(user):

    if user.total_deposit <= 0:
        return False, (
            "You must deposit at least "
            "$0.10 before withdrawing."
        )

    if user.wagered < user.total_deposit * 2:
        return False, (
            "You must wager 2x "
            "your deposits first."
        )

    return True, None


async def create_request(
    user,
    amount,
    address
):

    return {
        "user": user.discord_id,
        "amount": amount,
        "address": address,
        "status": "Pending"
    }

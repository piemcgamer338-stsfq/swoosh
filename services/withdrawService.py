from utils.constants import MIN_WITHDRAW_USD


async def request_withdraw(
    user,
    amount,
    address
):

    return {
        "approved": False,
        "amount": amount,
        "address": address,
        "status": "Waiting For Owner Approval"
    }

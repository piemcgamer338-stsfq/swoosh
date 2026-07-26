from database import get_session
from models import User


async def create_deposit_address(
    user_id
):

    # XPUB integration later
    return f"LTC_ADDRESS_{user_id}"


async def pending_deposit(
    txid
):

    return {
        "status": "Pending",
        "confirmations": 0
    }

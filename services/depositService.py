from config import LTC_XPUB


async def generate_deposit_address(user_id: int):

    """
    TODO:
    Generate deterministic LTC address
    from XPUB later.
    """

    return f"LTC_{user_id}"


async def get_confirmations(txid: str):

    """
    Placeholder.
    Replace with BlockCypher / Mempool API.
    """

    return 0


async def check_deposit(txid: str):

    confirmations = await get_confirmations(txid)

    return confirmations >= 1

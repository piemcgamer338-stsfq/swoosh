from config import OWNER_ID
from services import economy



def is_owner(user_id):

    return user_id == OWNER_ID



async def has_balance(
    user_id,
    amount
):

    balance = await economy.get_balance(
        user_id
    )

    return balance >= amount



async def can_bet(
    user_id,
    amount
):

    if amount <= 0:

        return False


    return await has_balance(
        user_id,
        amount
    )



def mention(user):

    return user.mention



def same_user(
    author,
    target
):

    return author.id == target.id

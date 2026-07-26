from services import economy
from services.gameHistory import add_game_history



async def win(
    user_id,
    game,
    bet,
    multiplier
):

    payout = bet * multiplier

    profit = payout - bet


    await economy.add_balance(
        user_id,
        payout
    )


    await add_game_history(
        user_id,
        game,
        bet,
        "WIN",
        multiplier,
        profit
    )


    return payout



async def lose(
    user_id,
    game,
    bet
):

    await add_game_history(
        user_id,
        game,
        bet,
        "LOSE",
        0,
        -bet
    )


    return 0



async def push(
    user_id,
    game,
    bet
):

    await economy.add_balance(
        user_id,
        bet
    )


    await add_game_history(
        user_id,
        game,
        bet,
        "PUSH",
        1,
        0
    )


    return bet

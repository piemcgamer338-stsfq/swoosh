import asyncio

from utils.fair import (
    generate_server_seed,
    hash_server_seed,
    generate_client_seed
)

from database import get_db


async def create_fair_game(
    user_id,
    game_type,
    amount
):

    server_seed = generate_server_seed()

    server_seed_hash = hash_server_seed(
        server_seed
    )

    client_seed = generate_client_seed()


    db = await get_db()


    game = await db.fetch_one(
        """
        INSERT INTO game_history
        (
            user_id,
            game_type,
            amount,
            server_seed,
            server_seed_hash,
            client_seed,
            nonce,
            result,
            multiplier,
            profit
        )
        VALUES
        (
            $1,$2,$3,$4,$5,$6,$7,$8,$9,$10
        )
        RETURNING *
        """,
        user_id,
        game_type,
        amount,
        server_seed,
        server_seed_hash,
        client_seed,
        0,
        "pending",
        0,
        0
    )


    return dict(game)




async def finish_fair_game(
    game_id,
    result,
    multiplier,
    profit
):

    db = await get_db()


    await db.execute(
        """
        UPDATE game_history

        SET
            result = $1,
            multiplier = $2,
            profit = $3

        WHERE id = $4
        """,
        result,
        multiplier,
        profit,
        game_id
    )

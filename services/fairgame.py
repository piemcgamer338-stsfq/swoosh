import asyncpg

from database import get_pool

from utils.fair import (
    generate_server_seed,
    hash_server_seed,
    generate_client_seed
)



async def create_fair_game(
    user_id,
    game,
    amount
):

    server_seed = generate_server_seed()

    server_seed_hash = hash_server_seed(
        server_seed
    )

    client_seed = generate_client_seed()


    pool = await get_pool()


    async with pool.acquire() as conn:


        row = await conn.fetchrow(
            """
            INSERT INTO game_history
            (
                discord_id,
                game,
                bet,
                result,
                multiplier,
                profit,
                server_seed_hash,
                server_seed,
                client_seed,
                nonce
            )

            VALUES
            (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6,
                $7,
                $8,
                $9,
                $10
            )

            RETURNING *
            """,

            user_id,
            game,
            amount,
            "pending",
            0,
            0,
            server_seed_hash,
            server_seed,
            client_seed,
            0
        )


    return dict(row)




async def finish_fair_game(
    game_id,
    result,
    multiplier,
    profit
):

    pool = await get_pool()


    async with pool.acquire() as conn:


        await conn.execute(
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

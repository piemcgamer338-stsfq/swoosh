from utils.fair import (
    generate_server_seed,
    hash_server_seed,
    generate_client_seed,
    generate_result
)

from database import get_pool



async def create_fair_game(
    user_id,
    game,
    bet
):

    server_seed = generate_server_seed()

    server_hash = hash_server_seed(
        server_seed
    )

    client_seed = generate_client_seed()


    pool = await get_pool()


    async with pool.acquire() as conn:

        game_id = await conn.fetchval(
            """
            INSERT INTO game_history (

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

            VALUES (

                $1,

                $2,

                $3,

                'Pending',

                0,

                0,

                $4,

                $5,

                $6,

                0

            )

            RETURNING id
            """,

            user_id,

            game,

            bet,

            server_hash,

            server_seed,

            client_seed

        )


    return {

        "id": game_id,

        "server_seed": server_seed,

        "client_seed": client_seed,

        "nonce": 0

    }



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

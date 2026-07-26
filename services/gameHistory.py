from database import get_pool


async def add_game_history(
    user_id,
    game,
    bet,
    result,
    multiplier,
    profit
):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO game_history
            (
                discord_id,
                game,
                bet,
                result,
                multiplier,
                profit
            )

            VALUES
            ($1,$2,$3,$4,$5,$6)
            """,

            user_id,
            game,
            bet,
            result,
            multiplier,
            profit
        )



async def get_stats(user_id):

    pool = await get_pool()

    async with pool.acquire() as conn:


        stats = await conn.fetchrow(
            """
            SELECT

            COUNT(*) AS total_games,

            COALESCE(SUM(bet),0) AS total_wager,

            COALESCE(SUM(
                CASE 
                    WHEN profit > 0 
                    THEN 1 
                    ELSE 0 
                END
            ),0) AS wins,


            COALESCE(SUM(
                CASE 
                    WHEN profit < 0 
                    THEN 1 
                    ELSE 0 
                END
            ),0) AS losses,


            COALESCE(SUM(profit),0) AS profit


            FROM game_history

            WHERE discord_id = $1
            """,

            user_id
        )


    return stats



async def get_recent_games(user_id, limit=5):

    pool = await get_pool()


    async with pool.acquire() as conn:


        games = await conn.fetch(
            """
            SELECT *

            FROM game_history

            WHERE discord_id = $1

            ORDER BY created_at DESC

            LIMIT $2
            """,

            user_id,
            limit
        )


    return games

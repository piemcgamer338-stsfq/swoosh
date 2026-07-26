from database import get_pool


async def create_user(user_id):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO users (
                discord_id,
                balance,
                wager,
                weekly_wager,
                rb_wager,
                deposited
            )
            VALUES ($1,0,0,0,0,0)

            ON CONFLICT (discord_id)
            DO NOTHING
            """,
            user_id
        )


async def get_user(user_id):

    await create_user(user_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        user = await conn.fetchrow(
            """
            SELECT *
            FROM users
            WHERE discord_id = $1
            """,
            user_id
        )

    return user



async def get_balance(user_id):

    user = await get_user(user_id)

    return user["balance"]



async def add_balance(user_id, amount):

    await create_user(user_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET balance = balance + $1
            WHERE discord_id = $2
            """,
            amount,
            user_id
        )



async def remove_balance(user_id, amount):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET balance = balance - $1
            WHERE discord_id = $2
            """,
            amount,
            user_id
        )



async def add_wager(user_id, amount):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users

            SET
            wager = wager + $1,
            weekly_wager = weekly_wager + $1,
            rb_wager = rb_wager + $1

            WHERE discord_id = $2
            """,
            amount,
            user_id
        )



async def reset_rb(user_id):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET rb_wager = 0
            WHERE discord_id = $1
            """,
            user_id
        )



async def reset_weekly(user_id):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET weekly_wager = 0
            WHERE discord_id = $1
            """,
            user_id
        )

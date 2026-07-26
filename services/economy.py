from database import get_pool


async def create_user(discord_id: int):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO users (discord_id)
            VALUES ($1)
            ON CONFLICT (discord_id) DO NOTHING
            """,
            discord_id
        )


async def get_user(discord_id: int):

    await create_user(discord_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        return await conn.fetchrow(
            """
            SELECT *
            FROM users
            WHERE discord_id = $1
            """,
            discord_id
        )


async def add_balance(discord_id: int, amount: float):

    await create_user(discord_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET balance = balance + $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )


async def remove_balance(discord_id: int, amount: float):

    await create_user(discord_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET balance = balance - $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )


async def set_balance(discord_id: int, amount: float):

    await create_user(discord_id)

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET balance = $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )


async def add_wager(discord_id: int, amount: float):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET
                wager = wager + $1,
                weekly_wager = weekly_wager + $1,
                rakeback_wager = rakeback_wager + $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )


async def add_win(discord_id: int, amount: float):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET won = won + $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )


async def add_loss(discord_id: int, amount: float):

    pool = await get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            UPDATE users
            SET lost = lost + $1
            WHERE discord_id = $2
            """,
            amount,
            discord_id
        )

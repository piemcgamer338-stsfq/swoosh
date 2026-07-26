import asyncpg
from config import DATABASE_URL

pool = None


async def connect_database():
    global pool

    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=10
    )

    async with pool.acquire() as conn:

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS users(

            discord_id BIGINT PRIMARY KEY,

            balance DOUBLE PRECISION DEFAULT 0,

            deposited DOUBLE PRECISION DEFAULT 0,

            wager DOUBLE PRECISION DEFAULT 0,

            weekly_wager DOUBLE PRECISION DEFAULT 0,

            rb_wager DOUBLE PRECISION DEFAULT 0,

            won DOUBLE PRECISION DEFAULT 0,

            lost DOUBLE PRECISION DEFAULT 0,

            affiliate BIGINT,

            created_at TIMESTAMP DEFAULT NOW()

        );

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS ranks(

            discord_id BIGINT PRIMARY KEY,

            current_rank INTEGER DEFAULT 0,

            claimed_rank INTEGER DEFAULT 0

        );

        """)

        print("✅ PostgreSQL Connected")


async def fetch(query, *args):

    async with pool.acquire() as conn:

        return await conn.fetch(query, *args)


async def fetchrow(query, *args):

    async with pool.acquire() as conn:

        return await conn.fetchrow(query, *args)


async def execute(query, *args):

    async with pool.acquire() as conn:

        return await conn.execute(query, *args)

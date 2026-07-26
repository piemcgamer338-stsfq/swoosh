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
        CREATE TABLE IF NOT EXISTS users (
            discord_id BIGINT PRIMARY KEY,

            balance DOUBLE PRECISION DEFAULT 0,
            vault DOUBLE PRECISION DEFAULT 0,

            deposited DOUBLE PRECISION DEFAULT 0,
            withdrawn DOUBLE PRECISION DEFAULT 0,

            wager DOUBLE PRECISION DEFAULT 0,
            weekly_wager DOUBLE PRECISION DEFAULT 0,
            rakeback_wager DOUBLE PRECISION DEFAULT 0,

            won DOUBLE PRECISION DEFAULT 0,
            lost DOUBLE PRECISION DEFAULT 0,

            affiliate_by BIGINT,
            affiliate_earned DOUBLE PRECISION DEFAULT 0,

            withdraw_allowed BOOLEAN DEFAULT FALSE,

            rank_claimed INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS threads (
            owner_id BIGINT PRIMARY KEY,
            thread_id BIGINT
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS deposits (
            id SERIAL PRIMARY KEY,
            discord_id BIGINT,
            txid TEXT,
            amount DOUBLE PRECISION,
            confirmations INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id SERIAL PRIMARY KEY,
            discord_id BIGINT,
            amount DOUBLE PRECISION,
            address TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            guild_id BIGINT PRIMARY KEY,
            admin_role BIGINT
        );
        """)

    print("✅ PostgreSQL Connected")


async def get_pool():
    return pool

import asyncpg

from config import DATABASE_URL


pool = None


async def get_pool():

    global pool

    if pool is None:

        pool = await asyncpg.create_pool(
            DATABASE_URL
        )

    return pool


async def setup_database():

    db = await get_pool()

    async with db.acquire() as conn:

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            discord_id BIGINT PRIMARY KEY,

            balance DOUBLE PRECISION DEFAULT 0,

            vault DOUBLE PRECISION DEFAULT 0,

            wager DOUBLE PRECISION DEFAULT 0,

            weekly_wager DOUBLE PRECISION DEFAULT 0,

            rb_wager DOUBLE PRECISION DEFAULT 0,

            deposited DOUBLE PRECISION DEFAULT 0,

            affiliate_by BIGINT,

            affiliate_earnings DOUBLE PRECISION DEFAULT 0,

            withdraw_allowed BOOLEAN DEFAULT FALSE,

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
        CREATE TABLE IF NOT EXISTS deposits (

            id SERIAL PRIMARY KEY,

            discord_id BIGINT,

            txid TEXT,

            amount DOUBLE PRECISION,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT NOW()

        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS threads (

            id SERIAL PRIMARY KEY,

            owner_id BIGINT,

            thread_id BIGINT UNIQUE,

            created_at TIMESTAMP DEFAULT NOW()

        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS house (

            id INTEGER PRIMARY KEY,

            balance DOUBLE PRECISION DEFAULT 80

        );
        """)

        await conn.execute("""
        INSERT INTO house(id,balance)

        VALUES(1,80)

        ON CONFLICT(id)

        DO NOTHING;
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS game_history (

            id SERIAL PRIMARY KEY,

            discord_id BIGINT,

            game TEXT,

            bet DOUBLE PRECISION,

            result TEXT,

            multiplier DOUBLE PRECISION,

            profit DOUBLE PRECISION,

            created_at TIMESTAMP DEFAULT NOW()

        );
        """)

    print("✅ Database ready")

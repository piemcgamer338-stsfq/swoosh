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


        # USERS

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                discord_id BIGINT PRIMARY KEY,

                balance DOUBLE PRECISION DEFAULT 0,

                vault DOUBLE PRECISION DEFAULT 0,

                wager DOUBLE PRECISION DEFAULT 0,

                weekly_wager DOUBLE PRECISION DEFAULT 0,

                rb_wager DOUBLE PRECISION DEFAULT 0,

                deposited DOUBLE PRECISION DEFAULT 0,

                withdrawn DOUBLE PRECISION DEFAULT 0,

                affiliate_by BIGINT,

                affiliate_earnings DOUBLE PRECISION DEFAULT 0,

                withdraw_allowed BOOLEAN DEFAULT FALSE,

                created_at TIMESTAMP DEFAULT NOW()

            );
            """
        )



        # DEPOSITS

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deposits (

                id SERIAL PRIMARY KEY,

                discord_id BIGINT,

                txid TEXT,

                amount DOUBLE PRECISION,

                status TEXT DEFAULT 'Pending',

                created_at TIMESTAMP DEFAULT NOW()

            );
            """
        )



        # WITHDRAWALS

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS withdrawals (

                id SERIAL PRIMARY KEY,

                discord_id BIGINT,

                amount DOUBLE PRECISION,

                address TEXT,

                status TEXT DEFAULT 'Pending',

                created_at TIMESTAMP DEFAULT NOW()

            );
            """
        )



        # THREADS

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS threads (

                id SERIAL PRIMARY KEY,

                owner_id BIGINT,

                thread_id BIGINT UNIQUE,

                created_at TIMESTAMP DEFAULT NOW()

            );
            """
        )



        # HOUSE

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS house (

                id INTEGER PRIMARY KEY,

                balance DOUBLE PRECISION DEFAULT 80

            );


            INSERT INTO house(
                id,
                balance
            )

            VALUES(
                1,
                80
            )

            ON CONFLICT(id)
            DO NOTHING;

            """
        )



        # GAME HISTORY

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS game_history (

                id SERIAL PRIMARY KEY,

                discord_id BIGINT,

                game TEXT,

                bet DOUBLE PRECISION,

                result TEXT,

                multiplier DOUBLE PRECISION DEFAULT 0,

                profit DOUBLE PRECISION DEFAULT 0,

                server_seed_hash TEXT,

                server_seed TEXT,

                client_seed TEXT,

                nonce INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT NOW()

            );
            """
        )



        # IMPORTANT:
        # Upgrade old databases automatically

        await conn.execute(
            """
            ALTER TABLE game_history
            ADD COLUMN IF NOT EXISTS server_seed_hash TEXT;

            ALTER TABLE game_history
            ADD COLUMN IF NOT EXISTS server_seed TEXT;

            ALTER TABLE game_history
            ADD COLUMN IF NOT EXISTS client_seed TEXT;

            ALTER TABLE game_history
            ADD COLUMN IF NOT EXISTS nonce INTEGER DEFAULT 0;
            """
        )


        print("✅ Database ready")

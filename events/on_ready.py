import discord

from database import setup_database


async def setup(bot):

    @bot.event
    async def on_ready():

        await setup_database()

        await bot.change_presence(
            activity=discord.Game(
                name="🎰 Swoosh Casino"
            )
        )


        print(
            f"✅ Logged in as {bot.user}"
        )

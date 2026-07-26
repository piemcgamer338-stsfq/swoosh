import os
import asyncio

import discord
from discord.ext import commands

from config import TOKEN, PREFIX


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=True
)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print("-----------------------------")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await bot.process_commands(message)


async def load_cogs():

    for file in os.listdir("./cogs"):

        if (
            file.endswith(".py")
            and not file.startswith("_")
        ):

            try:

                await bot.load_extension(
                    f"cogs.{file[:-3]}"
                )

                print(
                    f"Loaded {file}"
                )

            except Exception as e:

                print(
                    f"Failed to load {file}: {e}"
                )


async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio

import discord
from discord.ext import commands

from config import TOKEN, PREFIX
from database import setup_database


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

    print("=" * 50)
    print(f"✅ Logged in as {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌍 Connected Guilds: {len(bot.guilds)}")
    print("=" * 50)


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await bot.process_commands(message)


@bot.event
async def on_command(ctx):

    print(
        f"[COMMAND] {ctx.author} -> {ctx.command}"
    )


@bot.event
async def on_command_error(
    ctx,
    error
):

    print("\n" + "=" * 60)
    print("COMMAND ERROR")
    print(f"User    : {ctx.author}")
    print(f"Guild   : {ctx.guild}")
    print(f"Message : {ctx.message.content}")
    print(f"Error   : {repr(error)}")
    print("=" * 60 + "\n")

    try:
        await ctx.reply(
            f"❌ **{type(error).__name__}**\n```{error}```"
        )
    except Exception:
        pass


async def load_cogs():

    for file in os.listdir("./cogs"):

        if (
            file.endswith(".py")
            and
            not file.startswith("_")
        ):

            try:

                await bot.load_extension(
                    f"cogs.{file[:-3]}"
                )

                print(f"✅ Loaded {file}")

            except Exception as e:

                print(f"❌ Failed {file}")
                print(repr(e))


async def main():

    await setup_database()

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)


if __name__ == "__main__":

    asyncio.run(main())

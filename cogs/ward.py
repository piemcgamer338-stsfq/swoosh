import discord
from discord.ext import commands
import random
import asyncio

from services.economy import (
    get_balance,
    remove_balance,
    add_balance,
    add_wager
)

from services.fairgame import (
    create_fair_game,
    finish_fair_game
)

GREEN = "<:Based_GreenCoin:1530472181434155111>"


class Ward(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ward"
    )
    async def ward(
        self,
        ctx,
        amount: float
    ):

        if amount <= 0:
            return await ctx.reply(
                "Invalid bet amount."
            )

        balance = await get_balance(
            ctx.author.id
        )

        if balance < amount:
            return await ctx.reply(
                "You don't have enough balance."
            )

        fair = await create_fair_game(
            ctx.author.id,
            "ward",
            amount
        )

        await remove_balance(
            ctx.author.id,
            amount
        )

        await add_wager(
            ctx.author.id,
            amount
        )

        msg = await ctx.reply(
            "🎲 Rolling Dice..."
        )

        await asyncio.sleep(2)

        roll = random.randint(1, 100)

        if roll <= 60:

            # Lose
            player = random.randint(1, 5)
            dealer = random.randint(player + 1, 6)

            result = "Lose"
            winnings = 0
            profit = -amount
            colour = 0xE74C3C

        elif roll <= 99:

            # Win
            dealer = random.randint(1, 5)
            player = random.randint(dealer + 1, 6)

            winnings = amount * 2
            profit = amount

            await add_balance(
                ctx.author.id,
                winnings
            )

            result = "Win"
            colour = 0x2ECC71

        else:

            # Tie
            player = dealer = random.randint(1, 6)

            winnings = amount

            await add_balance(
                ctx.author.id,
                winnings
            )

            profit = 0
            result = "Tie"
            colour = 0xF1C40F

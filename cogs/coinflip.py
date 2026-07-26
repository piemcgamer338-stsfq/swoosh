from discord.ext import commands
import discord
import random

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
)


class Coinflip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="coinflip",
        aliases=["cf", "flip"]
    )
    async def coinflip(self, ctx, amount: float, choice: str):

        user_id = ctx.author.id


        choice = choice.lower()


        if choice not in ["heads", "tails", "h", "t"]:
            embed = discord.Embed(
                title="Coinflip",
                description="Choose `heads` or `tails`.",
                colour=0xE74C3C
            )

            return await ctx.reply(embed=embed)


        if choice in ["h"]:
            choice = "heads"

        if choice in ["t"]:
            choice = "tails"



        if amount <= 0:

            embed = discord.Embed(
                title="Coinflip",
                description="Bet must be above 0.",
                colour=0xE74C3C
            )

            return await ctx.reply(embed=embed)



        balance = await get_balance(user_id)


        if balance < amount:

            embed = discord.Embed(
                title="Coinflip",
                description="You don't have enough balance.",
                colour=0xE74C3C
            )

            return await ctx.reply(embed=embed)



        await remove_balance(
            user_id,
            amount
        )


        result = random.choice(
            [
                "heads",
                "tails"
            ]
        )


        if result == choice:

            winnings = amount * 2

            await add_balance(
                user_id,
                winnings
            )


            embed = discord.Embed(
                title="Coinflip Result",
                description=(
                    f"Coin landed on **{result}**\n\n"
                    f"You won **{winnings:,.2f} points**"
                ),
                colour=0x2ECC71
            )


        else:

            embed = discord.Embed(
                title="Coinflip Result",
                description=(
                    f"Coin landed on **{result}**\n\n"
                    f"You lost **{amount:,.2f} points**"
                ),
                colour=0xE74C3C
            )


        embed.set_footer(
            text="Swoosh Casino • Coinflip"
        )


        await ctx.reply(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Coinflip(bot)
    )

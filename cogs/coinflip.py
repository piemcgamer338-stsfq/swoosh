from discord.ext import commands
import discord

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
)

from services.fairgame import (
    create_fair_game,
    finish_fair_game
)

from utils.fair import coinflip_result


class Coinflip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="coinflip",
        aliases=["cf", "flip"]
    )
    async def coinflip(
        self,
        ctx,
        amount: float,
        choice: str
    ):

        user_id = ctx.author.id


        choice = choice.lower()


        if choice in ["h"]:
            choice = "heads"

        elif choice in ["t"]:
            choice = "tails"


        if choice not in [
            "heads",
            "tails"
        ]:

            return await ctx.reply(
                "Choose heads or tails."
            )


        if amount <= 0:

            return await ctx.reply(
                "Invalid amount."
            )


        balance = await get_balance(
            user_id
        )


        if balance < amount:

            return await ctx.reply(
                "You don't have enough points."
            )


        fair = await create_fair_game(
            user_id,
            "coinflip",
            amount
        )


        result = coinflip_result(
            fair["server_seed"],
            fair["client_seed"],
            fair["nonce"]
        )


        await remove_balance(
            user_id,
            amount
        )


        if result == choice:

            profit = amount

            await add_balance(
                user_id,
                amount * 2
            )

            text = (
                f"You won `{amount * 2:,.2f}` points\n\n"
                f"Result: **{result}**"
            )

            color = 0x2ECC71


        else:

            profit = -amount

            text = (
                f"You lost `{amount:,.2f}` points\n\n"
                f"Result: **{result}**"
            )

            color = 0xE74C3C



        await finish_fair_game(
            fair["id"],
            result,
            2,
            profit
        )


        embed = discord.Embed(
            title="Coinflip Result",
            description=text,
            colour=color
        )


        embed.add_field(
            name="Game ID",
            value=f"`#{fair['id']}`",
            inline=False
        )


        embed.add_field(
            name="Verification",
            value=f"`.verify {fair['id']}`",
            inline=False
        )


        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )


        await ctx.reply(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Coinflip(bot)
    )

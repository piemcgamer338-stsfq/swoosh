from discord.ext import commands
import discord
import asyncio

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
)

from services.fairgame import (
    create_fair_game,
    finish_fair_game
)

from utils.fair import limbo_result


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"


class Limbo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="limbo"
    )
    async def limbo(
        self,
        ctx,
        amount: float,
        target: float
    ):

        user_id = ctx.author.id


        if amount <= 0:

            return await ctx.reply(
                "Invalid bet amount."
            )


        if target < 1.01:

            return await ctx.reply(
                "Minimum multiplier is 1.01x."
            )


        if target > 1000:

            return await ctx.reply(
                "Maximum multiplier is 1000x."
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
            "limbo",
            amount
        )


        await remove_balance(
            user_id,
            amount
        )


        msg = await ctx.reply(
            "🚀 Launching Limbo..."
        )


        await asyncio.sleep(3)


        result = limbo_result(
            fair["server_seed"],
            fair["client_seed"],
            fair["nonce"]
        )


        won = result >= target


        if won:

            winnings = amount * target

            profit = winnings - amount


            await add_balance(
                user_id,
                winnings
            )


            title = "🚀 Limbo - You Won"

            description = (
                f"{GREEN_COIN} **Target:** `{target:.2f}x`\n"
                f"{GREEN_COIN} **Result:** `{result:.2f}x`\n\n"

                f"Nice! You won "
                f"{GREEN_COIN} `{winnings:,.2f}` points."
            )


            colour = 0x2ECC71


        else:

            winnings = 0

            profit = -amount


            title = "🚀 Limbo - You Lose"

            description = (
                f"{GREEN_COIN} **Target:** `{target:.2f}x`\n"
                f"{GREEN_COIN} **Result:** `{result:.2f}x`\n\n"

                "Better luck next time."
            )


            colour = 0xE74C3C



        await finish_fair_game(
            fair["id"],
            f"{result:.2f}x",
            target if won else 0,
            profit
        )


        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )


        embed.add_field(
            name="Bet",
            value=f"{GREEN_COIN} `{amount:,.2f}`",
            inline=True
        )


        embed.add_field(
            name="Multiplier",
            value=f"`{result:.2f}x`",
            inline=True
        )


        embed.add_field(
            name="🔒 Provably Fair",
            value=(
                f"Game ID: `{fair['id']}`\n"
                f"Verify: `.verify {fair['id']}`"
            ),
            inline=False
        )


        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )


        await msg.edit(
            content=None,
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Limbo(bot)
    )

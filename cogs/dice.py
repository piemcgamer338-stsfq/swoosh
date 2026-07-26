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

from utils.fair import dice_result


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="dice"
    )
    async def dice(
        self,
        ctx,
        amount: float,
        target: str
    ):

        user_id = ctx.author.id


        target = target.lower()


        if target not in [
            "high",
            "low"
        ]:

            return await ctx.reply(
                "Choose `high` or `low`."
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
            "dice",
            amount
        )


        await remove_balance(
            user_id,
            amount
        )


        # 3 second roll animation
        await ctx.reply(
            "Rolling dice..."
        )

        await asyncio.sleep(3)


        roll = dice_result(
            fair["server_seed"],
            fair["client_seed"],
            fair["nonce"]
        )


        if roll > 50:

            outcome = "high"

        else:

            outcome = "low"



        if outcome == target:

            multiplier = 1.95

            winnings = amount * multiplier

            profit = winnings - amount


            await add_balance(
                user_id,
                winnings
            )


            title = "🎲 Dice - You Won"

            description = (
                f"{GREEN_COIN} **Target:** {target}\n"
                f"{GREEN_COIN} **Outcome:** {outcome}\n\n"

                f"Nice! You won "
                f"{GREEN_COIN} `{winnings:,.2f}` points."
            )


            colour = 0x2ECC71



        else:

            winnings = 0

            profit = -amount


            title = "🎲 Dice - You Lose"


            description = (
                f"{GREEN_COIN} **Target:** {target}\n"
                f"{GREEN_COIN} **Outcome:** {outcome}\n\n"

                f"Better luck next time."
            )


            colour = 0xE74C3C



        await finish_fair_game(
            fair["id"],
            str(roll),
            multiplier if outcome == target else 0,
            profit
        )


        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )


        embed.add_field(
            name="Roll",
            value=f"`{roll}/100`",
            inline=True
        )


        embed.add_field(
            name="Bet",
            value=f"{GREEN_COIN} `{amount:,.2f}`",
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


        await ctx.reply(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Dice(bot)
    )

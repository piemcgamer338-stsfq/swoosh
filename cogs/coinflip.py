from discord.ext import commands
import discord

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

from utils.fair import coinflip_result


HEADS_IMAGE = "https://cdn.discordapp.com/attachments/1526285576393855088/1530849945312038993/c32d1eab-0b47-4684-baa2-59e77b8beaf8.png?ex=6a67129c&is=6a65c11c&hm=1d880fbcc591789325ed4b22bebce5f771[...]"

TAILS_IMAGE = "https://cdn.discordapp.com/attachments/1526285576393855088/1530849636108210236/1874c89b-4833-490d-9e24-2fa95d7dbf22.png?ex=6a671253&is=6a65c0d3&hm=71c6f09a4bb247fd5aafc8ad2b0bafb641[...]"



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


        if choice in ["h", "head"]:
            choice = "heads"

        elif choice in ["t", "tail"]:
            choice = "tails"


        if choice not in [
            "heads",
            "tails"
        ]:

            return await ctx.reply(
                "Choose `heads` or `tails`."
            )


        if amount <= 0:

            return await ctx.reply(
                "Invalid bet amount."
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

        await add_wager(
            user_id,
            amount
        )


        if result == choice:

            profit = amount

            await add_balance(
                user_id,
                amount * 2
            )


            description = (
                f"Result: **{result.upper()}**\n\n"
                f"You won **{amount * 2:,.2f} points**"
            )

            colour = 0x2ECC71


        else:

            profit = -amount


            description = (
                f"Result: **{result.upper()}**\n\n"
                f"You lost **{amount:,.2f} points**"
            )

            colour = 0xE74C3C



        await finish_fair_game(
            fair["id"],
            result,
            2,
            profit
        )


        embed = discord.Embed(
            title="Coinflip",
            description=description,
            colour=colour
        )


        embed.add_field(
            name="Game ID",
            value=f"`#{fair['id']}`",
            inline=True
        )


        embed.add_field(
            name="Verification",
            value=f"`.verify {fair['id']}`",
            inline=True
        )


        if result == "heads":

            embed.set_image(
                url=HEADS_IMAGE
            )

        else:

            embed.set_image(
                url=TAILS_IMAGE
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

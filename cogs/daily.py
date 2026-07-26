from discord.ext import commands
import discord

from services.economy import get_user, add_balance


class Daily(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="daily",
        aliases=["day"]
    )
    async def daily(self, ctx):

        user = await get_user(ctx.author.id)

        if user["balance"] < 1:
            return await ctx.reply(
                "❌ You need at least **1 Point** to claim your daily reward."
            )

        await add_balance(ctx.author.id, 2)

        embed = discord.Embed(
            title="🎁 Daily Reward",
            description=(
                "You claimed your daily reward!\n\n"
                "<:Based_GreenCoin:1530472181434155111> **+2.00 Points**"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Come back tomorrow!"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Daily(bot))

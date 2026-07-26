from discord.ext import commands
import discord

from database import get_pool


class Weekly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="weekly",
        aliases=["week"]
    )
    async def weekly(self, ctx):

        pool = await get_pool()

        async with pool.acquire() as conn:

            user = await conn.fetchrow(
                """
                SELECT weekly_wager
                FROM users
                WHERE discord_id = $1
                """,
                ctx.author.id
            )

            if user is None:
                return await ctx.reply(
                    "❌ You don't have an account yet."
                )

            cashback = round(user["weekly_wager"] * 0.005, 2)

            if cashback <= 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        title="🗓️ Weekly Cashback",
                        description=(
                            "You don't have any weekly cashback available.\n\n"
                            "📈 Wager more this week to earn cashback!"
                        ),
                        colour=0xE74C3C
                    )
                )

            await conn.execute(
                """
                UPDATE users
                SET
                    balance = balance + $1,
                    weekly_wager = 0
                WHERE discord_id = $2
                """,
                cashback,
                ctx.author.id
            )

        embed = discord.Embed(
            title="🗓️ Weekly Cashback",
            description=(
                f"You claimed your weekly cashback!\n\n"
                f"<:Based_GreenCoin:1530472181434155111> **+{cashback:.2f} Points**"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Weekly wager has been reset."
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Weekly(bot))

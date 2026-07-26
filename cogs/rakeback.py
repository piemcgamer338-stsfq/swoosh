from discord.ext import commands
import discord

from database import get_pool


class Rakeback(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="rakeback",
        aliases=["rb"]
    )
    async def rakeback(self, ctx):

        pool = await get_pool()

        async with pool.acquire() as conn:

            user = await conn.fetchrow(
                """
                SELECT rakeback_wager
                FROM users
                WHERE discord_id = $1
                """,
                ctx.author.id
            )

            if user is None:
                return await ctx.reply(
                    "❌ You don't have an account yet."
                )

            reward = round(user["rakeback_wager"] * 0.01, 2)

            if reward <= 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        title="💸 Rakeback",
                        description=(
                            "You don't have any rakeback available.\n\n"
                            "📈 Wager more to earn rakeback!"
                        ),
                        colour=0xE74C3C
                    )
                )

            await conn.execute(
                """
                UPDATE users
                SET
                    balance = balance + $1,
                    rakeback_wager = 0
                WHERE discord_id = $2
                """,
                reward,
                ctx.author.id
            )

        embed = discord.Embed(
            title="💸 Rakeback Claimed",
            description=(
                f"You claimed your rakeback!\n\n"
                f"<:Based_GreenCoin:1530472181434155111> **+{reward:.2f} Points**"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Rakeback wager has been reset."
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Rakeback(bot))

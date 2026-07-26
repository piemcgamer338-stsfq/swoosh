from discord.ext import commands
import discord

from config import OWNER_ID
from database import get_pool


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def owner_only():
        async def predicate(ctx):
            return ctx.author.id == OWNER_ID
        return commands.check(predicate)

    @commands.command(name="addbal")
    @owner_only()
    async def addbal(self, ctx, member: discord.Member, amount: float):

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE users
                SET balance = balance + $1
                WHERE discord_id = $2
                """,
                amount,
                member.id
            )

        await ctx.reply(
            f"✅ Added **{amount:.2f}** <:Based_GreenCoin:1530472181434155111> to {member.mention}"
        )

    @commands.command(name="resetbal")
    @owner_only()
    async def resetbal(self, ctx, member: discord.Member):

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE users
                SET balance = 0
                WHERE discord_id = $1
                """,
                member.id
            )

        await ctx.reply(
            f"✅ Reset {member.mention}'s balance."
        )

    @commands.command(name="allowwith")
    @owner_only()
    async def allowwith(self, ctx, member: discord.Member):

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE users
                SET withdraw_allowed = TRUE
                WHERE discord_id = $1
                """,
                member.id
            )

        await ctx.reply(
            f"✅ {member.mention} can now withdraw."
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))

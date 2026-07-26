from discord.ext import commands
import discord

from services.economy import (
    get_user,
    add_balance,
    remove_balance
)


class Tip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="tip"
    )
    async def tip(self, ctx, member: discord.Member, amount: float):

        if member.bot:
            return await ctx.reply(
                "❌ You can't tip bots."
            )

        if member.id == ctx.author.id:
            return await ctx.reply(
                "❌ You can't tip yourself."
            )

        if amount <= 0:
            return await ctx.reply(
                "❌ Enter a valid amount."
            )

        sender = await get_user(ctx.author.id)

        if sender["balance"] < amount:
            return await ctx.reply(
                "❌ You don't have enough balance."
            )

        await remove_balance(ctx.author.id, amount)
        await add_balance(member.id, amount)

        embed = discord.Embed(
            title="💸 Tip Sent",
            description=(
                f"{ctx.author.mention} tipped {member.mention}\n\n"
                f"<:Based_GreenCoin:1530472181434155111> **{amount:.2f} Points**"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Swoosh Casino"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Tip(bot))

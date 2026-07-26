from discord.ext import commands
import discord

from database import get_pool


class Withdraw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="withdraw",
        aliases=["with"]
    )
    async def withdraw(self, ctx, amount: float = None, *, address: str = None):

        if isinstance(ctx.channel, discord.DMChannel):
            return await ctx.reply(
                "❌ Please use this command inside the server."
            )

        if amount is None or address is None:
            return await ctx.reply(
                "Usage:\n```fix\n.withdraw <points> <ltc address>\n```"
            )

        if amount < 20:
            return await ctx.reply(
                "❌ Minimum withdrawal is **20 Points (£1.00)**."
            )

        pool = await get_pool()

        async with pool.acquire() as conn:

            user = await conn.fetchrow(
                """
                SELECT *
                FROM users
                WHERE discord_id = $1
                """,
                ctx.author.id
            )

            if not user:
                return await ctx.reply("❌ Account not found.")

            if user["balance"] < amount:
                return await ctx.reply(
                    "❌ You don't have enough balance."
                )

            if user["deposited"] <= 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        title="❌ Withdrawal Locked",
                        description=(
                            "You must deposit at least **£0.10** before withdrawing."
                        ),
                        colour=0xE74C3C
                    )
                )

            required = user["deposited"] * 2

            if user["wager"] < required:
                return await ctx.reply(
                    embed=discord.Embed(
                        title="❌ Wager Requirement",
                        description=(
                            f"You need to wager **{required:.2f} Points** before withdrawing.\n\n"
                            f"Current Wager: **{user['wager']:.2f} Points**"
                        ),
                        colour=0xE67E22
                    )
                )

            if not user["withdraw_allowed"]:
                return await ctx.reply(
                    embed=discord.Embed(
                        title="⏳ Awaiting Approval",
                        description=(
                            "Your account has not been approved for withdrawals yet.\n"
                            "Please wait for an administrator."
                        ),
                        colour=0xF1C40F
                    )
                )

            await conn.execute(
                """
                INSERT INTO withdrawals
                (discord_id, amount, address, status)
                VALUES ($1,$2,$3,'Pending')
                """,
                ctx.author.id,
                amount,
                address
            )

            await conn.execute(
                """
                UPDATE users
                SET
                    balance = balance - $1,
                    withdraw_allowed = FALSE
                WHERE discord_id = $2
                """,
                amount,
                ctx.author.id
            )

        embed = discord.Embed(
            title="<:deposit:1530474879185588386> Withdrawal Requested",
            description=(
                f"**Amount:** `{amount:.2f} Points`\n"
                f"**Address:**\n```{address}```\n\n"
                "Your withdrawal request has been submitted.\n"
                "Please wait while an administrator sends your LTC manually."
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Status: Pending Approval"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Withdraw(bot))

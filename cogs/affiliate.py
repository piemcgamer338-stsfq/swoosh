from discord.ext import commands
import discord

from database import get_pool


class Affiliate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="affiliate",
        aliases=["aff"]
    )
    async def affiliate(self, ctx, member: discord.Member = None):

        if member is None:

            embed = discord.Embed(
                title="🤝 Affiliate Program",
                description=(
                    "Invite your friends!\n\n"
                    "Your referral command:\n"
                    f"```fix\n.aff {ctx.author.id}\n```\n"
                    "Every **£1 wagered** by your referrals earns you **£0.01**."
                ),
                colour=0x2ECC71
            )

            embed.set_footer(
                text="Swoosh Casino Referral Program"
            )

            return await ctx.reply(embed=embed)

        if member.bot:
            return await ctx.reply(
                "❌ You cannot use a bot as your affiliate."
            )

        if member.id == ctx.author.id:
            return await ctx.reply(
                "❌ You cannot affiliate yourself."
            )

        pool = await get_pool()

        async with pool.acquire() as conn:

            user = await conn.fetchrow(
                """
                SELECT affiliate_by
                FROM users
                WHERE discord_id = $1
                """,
                ctx.author.id
            )

            if user and user["affiliate_by"]:
                return await ctx.reply(
                    "❌ You already have an affiliate."
                )

            await conn.execute(
                """
                UPDATE users
                SET affiliate_by = $1
                WHERE discord_id = $2
                """,
                member.id,
                ctx.author.id
            )

        embed = discord.Embed(
            title="✅ Affiliate Set",
            description=(
                f"You are now referred by {member.mention}.\n\n"
                "Every **£1** you wager gives them **£0.01**."
            ),
            colour=0x2ECC71
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Affiliate(bot))

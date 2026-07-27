import discord
from discord.ext import commands

from database import get_pool


GREEN_COIN = "<:GOLDEN_HEAD:1463050216574816309>"


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["profile", "p"]
    )
    async def stats(
        self,
        ctx,
        member: discord.Member = None
    ):

        member = member or ctx.author

        db = await get_pool()

        row = await db.fetchrow(
            """
            SELECT *
            FROM users
            WHERE discord_id = $1
            """,
            member.id
        )

        if row is None:
            return await ctx.reply(
                "User not registered."
            )

        balance = row["balance"]
        vault = row["vault"]
        wager = row["wager"]
        deposited = row["deposited"]
        withdrawn = row["withdrawn"]
        affiliate = row["affiliate_earnings"]

        embed = discord.Embed(
            title=f"{member.display_name}'s Statistics",
            colour=0x2ECC71
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.description = (
            "```ansi\n"
            "Profile Information\n"
            "```"
        )

        embed.add_field(
            name="Wallet",
            value=(
                f"**Balance**\n"
                f"{GREEN_COIN} `{balance:,.2f}`\n\n"
                f"**Vault**\n"
                f"{GREEN_COIN} `{vault:,.2f}`"
            ),
            inline=True
        )

        embed.add_field(
            name="Activity",
            value=(
                f"**Wagered**\n"
                f"{GREEN_COIN} `{wager:,.2f}`\n\n"
                f"**Affiliate Earned**\n"
                f"{GREEN_COIN} `{affiliate:,.2f}`"
            ),
            inline=True
        )

        embed.add_field(
            name="Transactions",
            value=(
                f"**Deposited**\n"
                f"{GREEN_COIN} `{deposited:,.2f}`\n\n"
                f"**Withdrawn**\n"
                f"{GREEN_COIN} `{withdrawn:,.2f}`"
            ),
            inline=False
        )

        embed.add_field(
            name="Account",
            value=(
                f"**Discord ID**\n"
                f"`{member.id}`\n\n"
                f"**Created**\n"
                f"`{member.created_at.strftime('%d %b %Y')}`"
            ),
            inline=False
        )

        embed.set_footer(
            text="Swoosh Casino • Statistics"
        )

        await ctx.reply(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        Stats(bot)
    )

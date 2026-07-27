import discord
from discord.ext import commands

from database import get_pool


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"
DEPOSITED = "<:E_purse:1530474784939311215>" 
WITHDRAW = "<:deposit:1530474879185588386>" 
DEPOSIT = " <:purse1:1530474754845179945> "
AFF = "<a:coinflip:1530475419877507234>" 
WAGARED = "<:casino_chips:1530572520506392746>"


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
                f"{DEPOSITED} `{vault:,.2f}`"
            ),
            inline=True
        )

        embed.add_field(
            name="Activity",
            value=(
                f"**Wagered**\n"
                f"{WAGARED} `{wager:,.2f}`\n\n"
                f"**Affiliate Earned**\n"
                f"{AFF} `{affiliate:,.2f}`"
            ),
            inline=True
        )

        embed.add_field(
            name="Transactions",
            value=(
                f"**Deposited**\n"
                f"{DEPOSIT} `{deposited:,.2f}`\n\n"
                f"**Withdrawn**\n"
                f"{WITHDRAW} `{withdrawn:,.2f}`"
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

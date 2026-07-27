import discord
from discord.ext import commands
import os

from database import get_pool
from utils.stats_image import create_stats_image


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

        avatar = member.display_avatar.url

        username = member.name

        balance = row["balance"]
        vault = row["vault"]
        wager = row["wager"]
        deposited = row["deposited"]
        withdrawn = row["withdrawn"]
        affiliate = row["affiliate_earnings"]

        join_date = member.created_at.strftime(
            "%d %b %Y"
        )

        join_date = member.joined_at.strftime("%d %b %Y") if member.joined_at else "Unknown"

        image_path = create_stats_image(
            avatar,
            username,
            balance,
            vault,
            wager,
            deposited,
            withdrawn,
            affiliate,
            join_date
        )

        file = discord.File(
            image_path,
            filename="stats.png"
        )

        await ctx.reply(
            file=file
        )

        try:
            os.remove(image_path)
        except:
            pass


async def setup(bot):
    await bot.add_cog(
        Stats(bot)
    )

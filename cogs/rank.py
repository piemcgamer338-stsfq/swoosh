from discord.ext import commands
import discord

from database import get_pool


RANKS = [
    ("Bronze", 0),
    ("Silver", 100),
    ("Gold", 500),
    ("Platinum", 1000),
    ("Diamond", 2500),
    ("Master", 5000),
    ("Legend", 10000),
    ("Champion", 25000),
]


class Rank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="rank",
        aliases=["level"]
    )
    async def rank(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        pool = await get_pool()

        async with pool.acquire() as conn:

            user = await conn.fetchrow(
                """
                SELECT wager
                FROM users
                WHERE discord_id = $1
                """,
                member.id
            )

        if not user:
            return await ctx.reply("❌ User not found.")

        wager = user["wager"]

        current = RANKS[0]
        next_rank = None

        for rank in RANKS:
            if wager >= rank[1]:
                current = rank
            else:
                next_rank = rank
                break

        if next_rank:
            progress = wager - current[1]
            needed = next_rank[1] - current[1]
            percent = min(progress / needed, 1)

            bar = (
                "🟩" * int(percent * 10)
                + "⬜" * (10 - int(percent * 10))
            )

            description = (
                f"**Current Rank**\n"
                f"`{current[0]}`\n\n"

                f"**Lifetime Wager**\n"
                f"`{wager:,.2f} Points`\n\n"

                f"**Next Rank**\n"
                f"`{next_rank[0]}` at `{next_rank[1]:,.2f}` Points\n\n"

                f"{bar}\n"
                f"`{progress:,.2f}/{needed:,.2f}`"
            )

        else:

            description = (
                f"🏆 **Maximum Rank Reached!**\n\n"
                f"`{current[0]}`\n\n"
                f"Lifetime Wager:\n"
                f"`{wager:,.2f} Points`"
            )

        embed = discord.Embed(
            title=f"🏅 {member.display_name}'s Rank",
            description=description,
            colour=0x2ECC71
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="Use .ranks to view every rank."
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Rank(bot))

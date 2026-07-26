from discord.ext import commands

from utils.embed import createEmbed


class Tos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="tos",
        aliases=["terms"]
    )
    async def tos(
        self,
        ctx
    ):

        embed = createEmbed(

            "📜 Swoosh Casino • Terms of Service",

            (
                "**By using Swoosh Casino you agree to the following:**\n\n"

                "• This bot uses **virtual Points**.\n"
                "• `1 Point = $0.005` value inside the bot.\n"
                "• Deposits and withdrawals are processed manually.\n"
                "• Attempting to exploit bugs may result in a permanent blacklist.\n"
                "• Alternate accounts used for farming rewards are prohibited.\n"
                "• Staff decisions are final.\n"
                "• Swoosh Casino may update these rules at any time.\n\n"

                "**Fairness**\n"
                "• Coinflip uses **Heads** or **Tails** only.\n"
                "• Provably Fair is available using `.pcf`.\n"
                "• Every game outcome is generated independently.\n\n"

                "**Withdrawals**\n"
                "• Minimum withdrawal: **$1.00**\n"
                "• You must wager **2x** your total deposits before withdrawing.\n"
                "• Withdrawals are reviewed by the owner before being marked as sent."
            )

        )

        await ctx.reply(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        Tos(bot)
    )

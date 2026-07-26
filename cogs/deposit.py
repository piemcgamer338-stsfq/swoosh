from discord.ext import commands
import discord

from config import LTC_ADDRESS, SOL_ADDRESS, USDT_ADDRESS


class Deposit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="deposit",
        aliases=["depo"]
    )
    async def deposit(self, ctx):

        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="<:purse1:1530474754845179945> Deposit Funds",
            description=(
                "**Minimum Deposit:** **£0.10**\n"
                "**1 Confirmation Required**\n\n"

                "## Litecoin (Recommended)\n"
                f"```{LTC_ADDRESS}```\n"

                "## Solana\n"
                f"```{SOL_ADDRESS}```\n"

                "## USDT (ERC20)\n"
                f"```{USDT_ADDRESS}```\n\n"

                "**After depositing:**\n"
                "Use `.depstatus <txid>` to check your deposit.\n\n"

                "⚠️ Sending to the wrong network may permanently lose your funds."
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Swoosh Casino • 1 Point = £0.005"
        )

        try:
            await ctx.author.send(embed=embed)

            await ctx.reply(
                "📩 I've sent the deposit addresses to your DMs.",
                delete_after=8
            )

        except discord.Forbidden:

            await ctx.reply(
                "❌ Please enable DMs from server members first.",
                delete_after=8
            )


async def setup(bot):
    await bot.add_cog(Deposit(bot))

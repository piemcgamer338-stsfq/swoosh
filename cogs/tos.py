from discord.ext import commands
import discord


class Terms(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="tos"
    )
    async def tos(self, ctx):

        embed = discord.Embed(
            title="📜 Swoosh Casino • Terms of Service",
            colour=0x2ECC71
        )

        embed.description = (
            "**1. General**\n"
            "By using **Swoosh Casino**, you agree to these Terms of Service.\n\n"

            "**2. Responsibility**\n"
            "• Gamble responsibly.\n"
            "• All bets are final.\n"
            "• Staff decisions are final.\n\n"

            "**3. Deposits & Withdrawals**\n"
            "**3.1 Minimum Deposit:** **£0.10**\n"
            "**3.2 Minimum Withdrawal:** **£1.00**\n"
            "**3.3 Wager Requirement:** **2×** your deposited amount.\n"
            "**3.4 Cryptocurrency:** Litecoin (LTC) is recommended.\n"
            "**3.5 Confirmations:** Deposits require **1 confirmation**.\n"
            "**3.6 Transactions are irreversible.** Always double-check your address.\n\n"

            "**4. Abuse**\n"
            "Using exploits, alternate accounts, automation or abusing bugs may result in your balance being reset and a permanent blacklist.\n\n"

            "**5. Provably Fair**\n"
            "Every game uses a Provably Fair system to ensure random and unbiased results.\n\n"

            "**6. Availability**\n"
            "The bot may be restarted or taken offline for updates without notice."
        )

        embed.set_footer(
            text="Swoosh Casino • Play Responsibly"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Terms(bot))thread.py insi

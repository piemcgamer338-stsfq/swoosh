from discord.ext import commands
import discord


class Guide(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="guide"
    )
    async def guide(self, ctx):

        embed = discord.Embed(
            title="📖 Welcome to Swoosh Casino",
            colour=0x2ECC71
        )

        embed.description = (
            "🎲 **Swoosh Casino** is a **Litecoin-based** Discord casino where you can bet, win and withdraw Litecoin.\n\n"

            "## 🪙 What are Points?\n"
            "• **1 Point = £0.005**\n"
            "• Used for every game.\n"
            "• Convert using `.price <amount>`.\n\n"

            "## 💸 Deposits & Withdrawals\n"
            "• `.deposit` → Receive deposit addresses.\n"
            "• Minimum Deposit: **£0.10**\n"
            "• `.withdraw <points> <address>`\n"
            "• Minimum Withdrawal: **£1.00**\n"
            "• Withdrawals require **2× deposit wager**.\n"
            "• LTC deposits require **1 confirmation**.\n\n"

            "## 🎁 Free Rewards\n"
            "• `.daily` → +2 Points every day.\n"
            "• `.weekly` → 0.50% Weekly Cashback.\n"
            "• `.rb` → 1% Rakeback.\n\n"

            "## 🎮 Games\n"
            "Use `.games` to see every available game.\n\n"

            "## 🛡️ Fairness\n"
            "Every game is **Provably Fair**.\n"
            "Your results are never manually changed.\n\n"

            "## 📜 Terms\n"
            "Use `.tos` to read the Terms of Service."
        )

        embed.set_footer(
            text="Swoosh Casino • Good Luck!"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Guide(bot))

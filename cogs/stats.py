from discord.ext import commands
import discord

from services.economy import get_user


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="stats",
        aliases=["stat"]
    )
    async def stats(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        user = await get_user(member.id)

        embed = discord.Embed(
            title=f"📊 {member.display_name}'s Statistics",
            colour=0x2ECC71
        )

        embed.description = (
            f"### 💰 Economy\n"
            f"> <:Based_GreenCoin:1530472181434155111> **Balance:** `{user['balance']:,.2f}` Points\n"
            f"> <:E_purse:1530474784939311215> **Vault:** `{user['vault']:,.2f}` Points\n"
            f"> <:purse1:1530474754845179945> **Deposited:** `{user['deposited']:,.2f}` Points\n"
            f"> <:deposit:1530474879185588386> **Withdrawn:** `{user['withdrawn']:,.2f}` Points\n\n"

            f"### 🎮 Gambling\n"
            f"> 📈 **Lifetime Wager:** `{user['wager']:,.2f}` Points\n"
            f"> 🗓️ **Weekly Wager:** `{user['weekly_wager']:,.2f}` Points\n"
            f"> 💸 **Rakeback Wager:** `{user['rakeback_wager']:,.2f}` Points\n\n"

            f"### 📈 Results\n"
            f"> 🟢 **Won:** `{user['won']:,.2f}` Points\n"
            f"> 🔴 **Lost:** `{user['lost']:,.2f}` Points\n\n"

            f"### 🤝 Affiliate\n"
            f"> 👤 **Referred By:** `{user['affiliate_by'] or 'None'}`\n"
            f"> 💰 **Earned:** `{user['affiliate_earned']:,.2f}` Points"
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))

from discord.ext import commands
import discord

from services.economy import get_user


class Balance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="balance",
        aliases=["bal", "b"]
    )
    async def balance(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        user = await get_user(member.id)

        balance = user["balance"]
        vault = user["vault"]

        usd = balance * 0.005
        ltc = balance * 0.0001

        embed = discord.Embed(
            title=f"{member.display_name}'s Balance",
            colour=0x2ECC71
        )

        embed.description = (
            f"<:Based_GreenCoin:1530472181434155111> **Wallet**\n"
            f"`{balance:,.2f}` Points\n\n"

            f"<:E_purse:1530474784939311215> **Vault**\n"
            f"`{vault:,.2f}` Points\n\n"

            f"💵 **Worth**\n"
            f"`£{usd:,.2f}`\n"
            f"`{ltc:.8f} LTC`"
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text="1 Point = £0.005 • 0.0001 LTC"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Balance(bot))

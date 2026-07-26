from discord.ext import commands
import discord

import requests


class Price(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="price",
        aliases=["rate"]
    )
    async def price(self, ctx, amount: float):

        try:

            data = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
            ).json()

            ltc_price = float(data["litecoin"]["usd"])

        except:

            return await ctx.reply(
                "❌ Couldn't fetch Litecoin price."
            )

        points = amount
        usd = points * 0.005
        ltc = usd / ltc_price

        embed = discord.Embed(
            title="💱 Point Calculator",
            colour=0x2ECC71
        )

        embed.description = (
            f"**Points**\n"
            f"`{points:,.2f}`\n\n"

            f"**USD**\n"
            f"`£{usd:,.2f}`\n\n"

            f"**Litecoin**\n"
            f"`{ltc:.8f} LTC`\n\n"

            f"**Current LTC Price**\n"
            f"`£{ltc_price:,.2f}`"
        )

        embed.set_footer(
            text="1 Point = £0.005"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Price(bot))

from discord.ext import commands
import discord

import requests


class DepositStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="depstatus",
        aliases=["tx", "status"]
    )
    async def depstatus(self, ctx, txid: str = None):

        if txid is None:
            return await ctx.reply(
                "Usage:\n```fix\n.depstatus <transaction id>\n```"
            )

        try:

            response = requests.get(
                f"https://chain.so/api/v2/get_tx/LTC/{txid}",
                timeout=10
            ).json()

            if response["status"] != "success":
                raise Exception()

            tx = response["data"]

            confirmations = int(tx["confirmations"])

            if confirmations >= 1:
                status = "🟢 Confirmed"
                colour = 0x2ECC71
            else:
                status = "🟡 Waiting for Confirmation"
                colour = 0xF1C40F

            embed = discord.Embed(
                title="<:purse1:1530474754845179945> Deposit Status",
                colour=colour
            )

            embed.description = (
                f"**Transaction ID**\n"
                f"```{txid}```\n"

                f"**Status**\n"
                f"`{status}`\n\n"

                f"**Confirmations**\n"
                f"`{confirmations}`\n\n"

                "**Network Required**\n"
                "`1 Confirmation`"
            )

            embed.set_footer(
                text="Deposits are credited after 1 confirmation."
            )

            await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(
                title="❌ Transaction Not Found",
                description=(
                    "The provided transaction couldn't be found.\n\n"
                    "Please make sure you entered the correct Litecoin TXID."
                ),
                colour=0xE74C3C
            )

            await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(DepositStatus(bot))

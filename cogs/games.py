from discord.ext import commands
import discord


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="games",
        aliases=["game"]
    )
    async def games(self, ctx):

        embed = discord.Embed(
            title="🎮 Swoosh Casino - Games",
            description=(
                "**CLASSIC GAMES**\n\n"

                "> <:blackjack:1530475467633852456> `.blackjack` `.bj`\n"
                "> <a:coinflip:1530475419877507234> `.cf`\n"
                "> <:dice6:1530475335118753842> `.bjdice`\n"
                "> <a:Rocket:1530573055645057267> `.limbo`\n"
                "> <:bomb:1530475533161463948> `.mines`\n"
                "> <:Roulette:1530475754297753701> `.roulette`\n\n"

                "**SPECIAL GAMES**\n\n"

                "> 📈 `.market`\n"
                "> 🪙 `.pcf`\n"
                "> 🃏 `.war`\n"
                "> 🎲 `.ward`\n"
                "> 🏎️ `.rush`\n\n"

                "**Every game is Provably Fair.**"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Swoosh Casino • Good Luck!"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))

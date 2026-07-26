from discord.ext import commands
import discord

from utils.embed import Embed


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help",
        aliases=["h"]
    )
    async def help(self, ctx):

        embed = discord.Embed(
            title="ℹ️ Help Command - Main Menu",
            description=(
                "Welcome to **Swoosh Casino**, the best Discord Casino Bot.\n\n"
                "💡 New here? Read `.guide`\n"
                "🎮 View our games using `.games`\n\n"

                "**UTILITY**                           **GAMES**\n"
                "> `.balance` `.bal` `.b`          > `.blackjack` `.bj`\n"
                "> `.stats` `.stat`                > `.cf`\n"
                "> `.daily`                        > `.bjdice`\n"
                "> `.weekly`                       > `.limbo`\n"
                "> `.rb` `.rakeback`              > `.mines`\n"
                "> `.deposit` `.depo`             > `.roulette`\n"
                "> `.withdraw`                    > `.market`\n"
                "> `.tip`                         > `.pcf`\n"
                "> `.affiliate` `.aff`           > `.rush`\n"
                "> `.price`                      > `.war`\n"
                "> `.depstatus`                  > `.ward`\n\n"

                "**THREADS**\n"
                "> `.thread create`\n"
                "> `.thread add`\n"
                "> `.thread remove`\n"
                "> `.thread delete`\n\n"

                "**OTHER**\n"
                "> `.guide`\n"
                "> `.tos`\n"
                "> `.rank`\n"
                "> `.ranks`\n"
            ),
            colour=0x2ECC71
        )

        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))

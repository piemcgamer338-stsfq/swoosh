from discord.ext import commands

from utils.embed import createEmbed


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="help",
        aliases=["h"]
    )
    async def help(
        self,
        ctx
    ):

        embed = createEmbed(

            "ℹ️ Help Command • Main Menu",

            (
                "Welcome to **Swoosh Casino**.\n\n"

                "New here?\n"
                "`.guide` - Learn how to use the bot\n"
                "`.games` - View all available games\n\n"


                "**UTILITY**\n"
                "```"
                "\n.balance      .bal      .b"
                "\n.stats        .stat     .p"
                "\n.daily"
                "\n.weekly"
                "\n.rb          .rakeback"
                "\n.deposit     .depo"
                "\n.withdraw"
                "\n.tip"
                "\n.affiliate   .aff"
                "\n.price"
                "\n.depstatus"
                "```\n"


                "**GAMES**\n"
                "```"
                "\n.blackjack   .bj"
                "\n.coinflip    .cf"
                "\n.dice"
                "\n.hilo"
                "\n.limbo"
                "\n.mines"
                "\n.roulette"
                "\n.rush"
                "\n.war"
                "\n.ward"
                "```\n"


                "**THREADS**\n"
                "```"
                "\n.thread create"
                "\n.thread add"
                "\n.thread remove"
                "\n.thread delete"
                "```\n"


                "**OTHER**\n"
                "```"
                "\n.guide"
                "\n.tos"
                "\n.rank"
                "\n.ranks"
                "```\n"


                "Use `.help <command>` for more details."
            )

        )


        await ctx.reply(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Help(bot)
    )

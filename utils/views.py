import discord


class HelpMenu(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=120
        )


        self.add_item(
            HelpSelect()
        )



class HelpSelect(discord.ui.Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Help Commands",
                description="View user commands",
                emoji="ℹ️"
            ),

            discord.SelectOption(
                label="Admin Commands",
                description="View staff commands",
                emoji="🛡️"
            ),

            discord.SelectOption(
                label="Casino Games",
                description="View available games",
                emoji="🎰"
            )

        ]


        super().__init__(
            placeholder="Select a category...",
            options=options
        )



    async def callback(
        self,
        interaction: discord.Interaction
    ):

        value = self.values[0]


        if value == "Help Commands":

            embed = discord.Embed(
                title="ℹ️ Help Commands",
                description=(
                    "`.bal` - Check balance\n"
                    "`.stats` - View statistics\n"
                    "`.daily` - Daily reward\n"
                    "`.weekly` - Weekly cashback\n"
                    "`.rb` - Rakeback\n"
                    "`.deposit` - Deposit LTC\n"
                    "`.withdraw` - Withdraw LTC\n"
                    "`.tip` - Send points"
                ),
                colour=0x2ECC71
            )


        elif value == "Admin Commands":

            embed = discord.Embed(
                title="🛡️ Admin Commands",
                description=(
                    "`.addbal @user amount`\n"
                    "`.resetbal @user`\n"
                    "`.allowwith @user`"
                ),
                colour=0x2ECC71
            )


        else:

            embed = discord.Embed(
                title="🎰 Casino Games",
                description=(
                    "`.bj` - Blackjack\n"
                    "`.cf` - Coinflip\n"
                    "`.limbo` - Limbo\n"
                    "`.mines` - Mines\n"
                    "`.roulette` - Roulette\n"
                    "`.market` - Prediction Market"
                ),
                colour=0x2ECC71
            )


        await interaction.response.edit_message(
            embed=embed
        )

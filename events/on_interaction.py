async def setup(bot):

    @bot.event
    async def on_interaction(
        interaction
    ):

        if interaction.type.name == "component":

            pass

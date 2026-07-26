async def setup(bot):

    @bot.event
    async def on_message(message):

        if message.author.bot:
            return


        await bot.process_commands(
            message
        )

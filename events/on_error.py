from utils.logger import error


async def setup(bot):

    @bot.event
    async def on_error(
        event,
        *args,
        **kwargs
    ):

        error(
            f"Event Error: {event}"
        )

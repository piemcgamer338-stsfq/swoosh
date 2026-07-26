import os
import importlib


async def load_events(bot):

    for file in os.listdir(
        "./events"
    ):

        if file.endswith(".py"):

            module = importlib.import_module(
                f"events.{file[:-3]}"
            )


            if hasattr(
                module,
                "setup"
            ):

                await module.setup(
                    bot
                )


            print(
                f"Loaded event: {file}"
            )

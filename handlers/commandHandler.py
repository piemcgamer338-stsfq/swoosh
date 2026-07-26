import os


async def load_commands(bot):

    for file in os.listdir(
        "./cogs"
    ):

        if file.endswith(".py"):

            try:

                await bot.load_extension(
                    f"cogs.{file[:-3]}"
                )

                print(
                    f"Loaded command: {file}"
                )

            except Exception as e:

                print(
                    f"Failed loading {file}: {e}"
                )

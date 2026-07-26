async def reload_cog(
    bot,
    name
):

    await bot.reload_extension(
        f"cogs.{name}"
    )


async def unload_cog(
    bot,
    name
):

    await bot.unload_extension(
        f"cogs.{name}"
    )


async def load_cog(
    bot,
    name
):

    await bot.load_extension(
        f"cogs.{name}"
    )

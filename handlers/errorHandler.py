import discord


async def handle_error(
    ctx,
    error
):

    embed = discord.Embed(
        title="❌ Error",
        description=str(error),
        colour=0xE74C3C
    )


    await ctx.reply(
        embed=embed
    )

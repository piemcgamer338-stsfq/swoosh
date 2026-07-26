import discord


COLOR = 0x2ECC71



def game_start(
    title,
    description
):

    return discord.Embed(
        title=f"🎰 {title}",
        description=description,
        colour=COLOR
    )



def game_result(
    title,
    result,
    profit
):

    embed = discord.Embed(
        title=title,
        colour=COLOR
    )


    embed.description = (
        f"**Result**\n"
        f"`{result}`\n\n"

        f"**Profit**\n"
        f"`{profit:+.2f} Points`"
    )


    return embed

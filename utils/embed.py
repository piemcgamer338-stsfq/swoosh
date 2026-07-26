import discord
from datetime import datetime


COLOR_MAIN = 0x2ECC71
COLOR_ERROR = 0xE74C3C
COLOR_WARNING = 0xF1C40F



def createEmbed(
    title,
    description,
    color=COLOR_MAIN
):

    embed = discord.Embed(
        title=title,
        description=description,
        colour=color,
        timestamp=datetime.utcnow()
    )


    embed.set_footer(
        text="Swoosh Casino • 1 Point = £0.005 LTC"
    )


    return embed



def success(message):

    return createEmbed(
        "✅ Success",
        message,
        COLOR_MAIN
    )



def error(message):

    return createEmbed(
        "❌ Error",
        message,
        COLOR_ERROR
    )



def warning(message):

    return createEmbed(
        "⚠️ Warning",
        message,
        COLOR_WARNING
    )



def info(message):

    return createEmbed(
        "ℹ️ Information",
        message,
        COLOR_MAIN
    )

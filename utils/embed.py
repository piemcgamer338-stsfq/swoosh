import discord


class Embed:

    @staticmethod
    def success(description: str):

        return discord.Embed(
            colour=0x2ECC71,
            description=f"✅ {description}"
        )


    @staticmethod
    def error(description: str):

        return discord.Embed(
            colour=0xE74C3C,
            description=f"❌ {description}"
        )


    @staticmethod
    def warning(description: str):

        return discord.Embed(
            colour=0xF1C40F,
            description=f"⚠️ {description}"
        )


    @staticmethod
    def info(title: str, description: str):

        embed = discord.Embed(
            title=title,
            description=description,
            colour=0x5865F2
        )

        embed.set_footer(
            text="Swoosh Casino"
        )

        return embed


    @staticmethod
    def casino(title: str, description: str):

        embed = discord.Embed(
            title=title,
            description=description,
            colour=0x00B894
        )

        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )

        return embed


    @staticmethod
    def game(title: str, description: str):

        embed = discord.Embed(
            title=title,
            description=description,
            colour=0x0099FF
        )

        embed.set_footer(
            text="Good Luck!"
        )

        return embed

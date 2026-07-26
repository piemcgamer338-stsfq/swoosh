import discord
from discord.ext import commands

from services.economy import get_balance
from services.rain import (
    ACTIVE_RAIN,
    create_rain
)

from utils.rain_time import (
    parse_time,
    format_time
)

GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"


class RainView(discord.ui.View):

    def __init__(self, rain):
        super().__init__(timeout=None)
        self.rain = rain

    @discord.ui.button(
        label="☔ Join Rain",
        style=discord.ButtonStyle.success
    )
    async def join(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.rain.finished:

            return await interaction.response.send_message(
                "Rain already ended.",
                ephemeral=True
            )


        if not self.rain.join(
            interaction.user.id
        ):

            return await interaction.response.send_message(
                "You can't join this rain.",
                ephemeral=True
            )


        embed = self.rain.message.embeds[0]

        embed.set_field_at(
            3,
            name="Participants",
            value=str(
                len(self.rain.participants)
            ),
            inline=True
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )


class Rain(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def rain(
        self,
        ctx,
        amount: float,
        duration: str
    ):

        if ACTIVE_RAIN:

            return await ctx.reply(
                "❌ A rain is already active."
            )


        if amount < 100:

            return await ctx.reply(
                "Minimum rain is 100 points."
            )


        if amount > 10000:

            return await ctx.reply(
                "Maximum rain is 10,000 points."
            )


        seconds = parse_time(
            duration
        )

        if not seconds:

            return await ctx.reply(
                "Use formats like 30s, 5m or 1h."
            )


        balance = await get_balance(
            ctx.author.id
        )

        if balance < amount:

            return await ctx.reply(
                "Not enough balance."
            )


        embed = discord.Embed(
            title="🌧 Rain Started",
            colour=0x3498DB
        )

        embed.add_field(
            name="Host",
            value=ctx.author.mention,
            inline=True
        )

        embed.add_field(
            name="Prize Pool",
            value=f"{GREEN_COIN} `{amount:,.2f}`",
            inline=True
        )

        embed.add_field(
            name="Time Left",
            value=format_time(seconds),
            inline=True
        )

        embed.add_field(
            name="Participants",
            value="0",
            inline=True
        )


        msg = await ctx.reply(
            embed=embed
        )


        rain = await create_rain(
            ctx.author.id,
            amount,
            seconds,
            ctx.channel,
            msg
        )


        rain.message = msg

        await msg.edit(
            embed=embed,
            view=RainView(rain)
        )


async def setup(bot):

    await bot.add_cog(
        Rain(bot)
    )

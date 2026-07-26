import os
import discord

from discord.ext import commands

from discord.ui import View, Button

from services.hilo import HiLoGame

from utils.hilo_image import create_hilo_image

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
)


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"
DEPOSIT_EMOJI = "<:deposit:1530123456789012345>"

ACTIVE_GAMES = {}


class HiLoView(View):

    def __init__(
        self,
        game,
        author
    ):

        super().__init__(
            timeout=120
        )

        self.game = game
        self.author = author


    async def interaction_check(
        self,
        interaction: discord.Interaction
    ):

        if interaction.user.id != self.author.id:

            await interaction.response.send_message(
                "This isn't your game.",
                ephemeral=True
            )

            return False

        return True


    async def update_embed(
        self,
        interaction,
        title=None,
        description=None,
        finished=False
    ):

        image_path = create_hilo_image(
            self.game.current
        )

        file = discord.File(
            image_path,
            filename="card.png"
        )

        embed = discord.Embed(
            title=title or "HiLo",
            colour=0x2ECC71
        )

        embed.description = (
            description
            or
            (
                f"💸 **Initial Bet:** {GREEN_COIN} `{self.game.bet:,.2f}`\n"
                f"🔥 **Current Multiplier:** `{self.game.multiplier:.2f}x`\n"
                f"💰 **Potential Payout:** {GREEN_COIN} `{self.game.payout:,.2f}`\n\n"
                f"🃏 **Active Card:** `{self.game.current.display}`"
            )
        )

        embed.set_image(
            url="attachment://card.png"
        )

        if finished:

            for child in self.children:
                child.disabled = True

        await interaction.response.edit_message(
            embed=embed,
            attachments=[file],
            view=self
        )

        try:
            os.remove(image_path)
        except:
            pass


    @discord.ui.button(
        label="Higher",
        style=discord.ButtonStyle.success
    )
    async def higher(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        result, card = self.game.guess(
            "higher"
        )

        if result == "win":

            await self.update_embed(
                interaction
            )

            return

        if result == "tie":

            await self.update_embed(
                interaction,
                description=(
                    "Same value! Card redrawn.\n\n"
                    f"🃏 `{card.display}`"
                )
            )

            return

        await self.update_embed(
            interaction,
            title="HiLo - You Lost",
            description=(
                f"Previous Card: `{self.game.previous.display}`\n"
                f"New Card: `{card.display}`\n\n"
                "Better luck next time."
            ),
            finished=True
        )
    @discord.ui.button(
        label="Lower",
        style=discord.ButtonStyle.success
    )
    async def lower(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        result, card = self.game.guess(
            "lower"
        )

        if result == "win":

            await self.update_embed(
                interaction
            )

            return


        if result == "tie":

            await self.update_embed(
                interaction,
                description=(
                    "Same value! Card redrawn.\n\n"
                    f"🃏 `{card.display}`"
                )
            )

            return


        await self.update_embed(
            interaction,
            title="HiLo - You Lost",
            description=(
                f"Previous Card: `{self.game.previous.display}`\n"
                f"New Card: `{card.display}`\n\n"
                "Better luck next time."
            ),
            finished=True
        )


    @discord.ui.button(
        emoji=DEPOSIT_EMOJI,
        label="Cashout",
        style=discord.ButtonStyle.danger
    )
    async def cashout(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        winnings = self.game.cashout()

        profit = winnings - self.game.bet

        await add_balance(
            self.author.id,
            winnings
        )


        image_path = create_hilo_image(
            self.game.current
        )

        file = discord.File(
            image_path,
            filename="card.png"
        )


        embed = discord.Embed(
            title="HiLo - Cashed Out",
            colour=0x2ECC71
        )

        embed.description = (
            f"💸 **Initial Bet:** {GREEN_COIN} `{self.game.bet:,.2f}`\n"
            f"🔥 **Final Multiplier:** `{self.game.multiplier:.2f}x`\n"
            f"💰 **Payout:** {GREEN_COIN} `{winnings:,.2f}`\n\n"
            f"📈 **Profit:** {GREEN_COIN} `{profit:,.2f}`\n\n"
            f"🃏 **Final Card:** `{self.game.current.display}`"
        )

        embed.set_image(
            url="attachment://card.png"
        )


        for child in self.children:
            child.disabled = True


        await interaction.response.edit_message(
            embed=embed,
            attachments=[file],
            view=self
        )

        try:
            os.remove(
                image_path
            )
        except:
            pass


class HiLo(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot


    @commands.command(
        aliases=["hl"]
    )
    async def hilo(
        self,
        ctx,
        amount: float
    ):

        if amount <= 0:

            return await ctx.reply(
                "Invalid bet."
            )


        balance = await get_balance(
            ctx.author.id
        )


                if balance < amount:

            return await ctx.reply(
                "Not enough balance."
            )


        await remove_balance(
            ctx.author.id,
            amount
        )


        game = HiLoGame(
            ctx.author.id,
            amount
        )

        ACTIVE_GAMES[
            ctx.author.id
        ] = game


        image_path = create_hilo_image(
            game.current
        )

        file = discord.File(
            image_path,
            filename="card.png"
        )

        embed = discord.Embed(
            title="HiLo",
            colour=0x2ECC71
        )

        embed.description = (
            f"💸 **Initial Bet:** {GREEN_COIN} `{amount:,.2f}`\n"
            f"🔥 **Current Multiplier:** `{game.multiplier:.2f}x`\n"
            f"💰 **Potential Payout:** {GREEN_COIN} `{game.payout:,.2f}`\n\n"
            f"🃏 **Active Card:** `{game.current.display}`"
        )

        embed.set_image(
            url="attachment://card.png"
        )

        embed.set_footer(
            text="Choose Higher or Lower"
        )


        await ctx.reply(
            embed=embed,
            file=file,
            view=HiLoView(
                game,
                ctx.author
            )
        )


        try:
            os.remove(
                image_path
            )
        except:
            pass


async def setup(bot):

    await bot.add_cog(
        HiLo(bot)
    )

import discord

from discord.ext import commands
from discord.ui import View, Button

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
)

from services.fairgame import (
    create_fair_game,
    finish_fair_game
)

from utils.mines import generate_mines


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"


class MinesGame:

    def __init__(
        self,
        user_id,
        amount,
        fair
    ):

        self.user_id = user_id
        self.amount = amount

        self.fair_id = fair["id"]

        self.mines = generate_mines(
            fair["server_seed"],
            fair["client_seed"],
            fair["nonce"],
            25,
            3
        )

        self.safe = 0
        self.finished = False
        self.clicked = []



class MinesButton(Button):

    def __init__(
        self,
        index,
        game
    ):

        super().__init__(
            label="⬜",
            style=discord.ButtonStyle.secondary,
            row=index // 5
        )

        self.index = index
        self.game = game



    async def callback(
        self,
        interaction
    ):


        if interaction.user.id != self.game.user_id:

            return await interaction.response.send_message(
                "This is not your game.",
                ephemeral=True
            )


        if self.game.finished:

            return await interaction.response.send_message(
                "Game already ended.",
                ephemeral=True
            )


        await interaction.response.defer()


        self.game.clicked.append(
            self.index
        )


        if self.index in self.game.mines:

            self.game.finished = True


            for child in self.view.children:

                child.disabled = True


            self.label = "💣"
            self.style = discord.ButtonStyle.danger



            embed = discord.Embed(
                title="Mines - You Lost",
                colour=0xE74C3C
            )


            embed.description = (
                f"{GREEN_COIN} Bet: `{self.game.amount:,.2f}`\n\n"
                "You hit a mine."
            )


            await finish_fair_game(
                self.game.fair_id,
                "mine",
                0,
                -self.game.amount
            )


            return await interaction.edit_original_response(
                embed=embed,
                view=self.view
            )



        self.game.safe += 1


        self.label = "💎"
        self.style = discord.ButtonStyle.success


        multiplier = round(
            1.20 + (self.game.safe * 0.20),
            2
        )


        winnings = (
            self.game.amount * multiplier
        )


        embed = discord.Embed(
            title="Mines",
            colour=0x2ECC71
        )


        embed.description = (

            f"{GREEN_COIN} Bet: `{self.game.amount:,.2f}`\n"
            f"💎 Diamonds: `{self.game.safe}`\n"
            f"Multiplier: `{multiplier}x`\n\n"

            "Find more diamonds or cash out."
        )


        await interaction.edit_original_response(
            embed=embed,
            view=self.view
        )




class CashoutButton(Button):

    def __init__(
        self,
        game
    ):

        super().__init__(
            label="Cashout",
            style=discord.ButtonStyle.primary,
            row=5
        )

        self.game = game



    async def callback(
        self,
        interaction
    ):


        if interaction.user.id != self.game.user_id:

            return await interaction.response.send_message(
                "This is not your game.",
                ephemeral=True
            )


        if self.game.finished:

            return await interaction.response.send_message(
                "Game already ended.",
                ephemeral=True
            )


        multiplier = round(
            1.20 + (self.game.safe * 0.20),
            2
        )


        winnings = (
            self.game.amount * multiplier
        )


        await add_balance(
            self.game.user_id,
            winnings
        )


        self.game.finished = True


        await finish_fair_game(
            self.game.fair_id,
            f"{multiplier}x",
            multiplier,
            winnings - self.game.amount
        )


        for child in self.view.children:

            child.disabled = True



        embed = discord.Embed(
            title="Mines - Cashed Out",
            colour=0x2ECC71
        )


        embed.description = (

            f"{GREEN_COIN} Won: `{winnings:,.2f}`\n"
            f"Multiplier: `{multiplier}x`"

        )


        await interaction.response.edit_message(
            embed=embed,
            view=self.view
        )




class MinesView(View):

    def __init__(
        self,
        game
    ):

        super().__init__(
            timeout=300
        )

        self.game = game


        for i in range(25):

            self.add_item(
                MinesButton(
                    i,
                    game
                )
            )


        self.add_item(
            CashoutButton(
                game
            )
        )




class Mines(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot



    @commands.command(
        name="mines"
    )
    async def mines(
        self,
        ctx,
        amount: float
    ):


        user_id = ctx.author.id


        if amount <= 0:

            return await ctx.reply(
                "Invalid amount."
            )


        balance = await get_balance(
            user_id
        )


        if balance < amount:

            return await ctx.reply(
                "Not enough balance."
            )



        fair = await create_fair_game(
            user_id,
            "mines",
            amount
        )


        await remove_balance(
            user_id,
            amount
        )


        game = MinesGame(
            user_id,
            amount,
            fair
        )


        embed = discord.Embed(
            title="Mines",
            colour=0x3498DB
        )


        embed.description = (

            f"{GREEN_COIN} Bet: `{amount:,.2f}`\n\n"
            "Click diamonds and avoid mines."

        )


        await ctx.reply(
            embed=embed,
            view=MinesView(game)
        )



async def setup(
    bot
):

    await bot.add_cog(
        Mines(bot)
    )

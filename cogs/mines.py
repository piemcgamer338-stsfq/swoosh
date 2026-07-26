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

# Change this if your deposit emoji ID is different
CASHOUT_EMOJI = "💰"



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
                "Game ended.",
                ephemeral=True
            )


        await interaction.response.defer()



        if self.index in self.game.mines:

            self.game.finished = True


            for child in self.view.children:
                child.disabled = True


            self.label = "💣"
            self.style = discord.ButtonStyle.danger


            await finish_fair_game(
                self.game.fair_id,
                "mine",
                0,
                -self.game.amount
            )


            embed = discord.Embed(
                title="Mines - You Lost",
                colour=0xE74C3C
            )


            embed.description = (
                f"{GREEN_COIN} Bet: `{self.game.amount:,.2f}`\n\n"
                "You hit a mine."
            )


            return await interaction.edit_original_response(
                embed=embed,
                view=self.view
            )



        self.safe += 1


        self.label = "💎"
        self.style = discord.ButtonStyle.success


        multiplier = round(
            1.15 + (self.safe * 0.18),
            2
        )


        embed = discord.Embed(
            title="Mines",
            colour=0x2ECC71
        )


        embed.description = (
            f"{GREEN_COIN} Bet: `{self.game.amount:,.2f}`\n"
            f"💎 Diamonds: `{self.safe}`\n"
            f"Multiplier: `{multiplier}x`\n\n"
            f"React {CASHOUT_EMOJI} to cashout."
        )


        await interaction.edit_original_response(
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




class Mines(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

        self.games = {}



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


        self.games[user_id] = game


        embed = discord.Embed(
            title="Mines",
            colour=0x3498DB
        )


        embed.description = (
            f"{GREEN_COIN} Bet: `{amount:,.2f}`\n\n"
            f"React {CASHOUT_EMOJI} anytime to cashout."
        )


        msg = await ctx.reply(
            embed=embed,
            view=MinesView(game)
        )


        await msg.add_reaction(
            CASHOUT_EMOJI
        )


        game.message_id = msg.id



    @commands.Cog.listener()
    async def on_reaction_add(
        self,
        reaction,
        user
    ):


        if user.bot:
            return


        if str(reaction.emoji) != CASHOUT_EMOJI:
            return


        if user.id not in self.games:
            return


        game = self.games[user.id]


        if game.finished:
            return


        multiplier = round(
            1.15 + (game.safe * 0.18),
            2
        )


        winnings = (
            game.amount * multiplier
        )


        await add_balance(
            user.id,
            winnings
        )


        game.finished = True


        await finish_fair_game(
            game.fair_id,
            f"{multiplier}x",
            multiplier,
            winnings - game.amount
        )


        embed = discord.Embed(
            title="Mines - Cashed Out",
            colour=0x2ECC71
        )


        embed.description = (
            f"{GREEN_COIN} Won: `{winnings:,.2f}`\n"
            f"Multiplier: `{multiplier}x`"
        )


        channel = reaction.message.channel


        await reaction.message.edit(
            embed=embed,
            view=None
        )



async def setup(bot):

    await bot.add_cog(
        Mines(bot)
    )

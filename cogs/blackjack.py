import discord
from discord.ext import commands
import os

from services.economy import (
    get_balance,
    remove_balance,
    add_balance,
    add_wager
)

from services.fairgame import (
    create_fair_game,
    finish_fair_game
)

from utils.blackjack_engine import (
    create_deck,
    draw_card,
    hand_value,
    dealer_play,
    compare,
    is_blackjack
)

from utils.blackjack_image import (
    create_blackjack_image
)


GREEN_COIN = "<:Based_GreenCoin:1530472181434155111>"


class BlackjackView(discord.ui.View):

    def __init__(
        self,
        ctx,
        fair,
        deck,
        player_hand,
        dealer_hand,
        bet
    ):
        super().__init__(
            timeout=120
        )

        self.ctx = ctx
        self.fair = fair
        self.deck = deck
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.bet = bet
        self.finished = False


    async def send_result(
        self,
        interaction,
        title,
        colour,
        hide_dealer=False
    ):

        image = create_blackjack_image(
            self.player_hand,
            self.dealer_hand,
            hide_dealer
        )

        file = discord.File(
            image,
            filename="blackjack.png"
        )


        embed = discord.Embed(
            title=title,
            colour=colour
        )


        embed.description = (
            f"{GREEN_COIN} **Bet:** `{self.bet:,.2f}`\n\n"
            f"**Player:** `{hand_value(self.player_hand)}`\n"
            f"**Dealer:** `{hand_value(self.dealer_hand) if not hide_dealer else '?'}`"
        )


        embed.set_image(
            url="attachment://blackjack.png"
        )


        await interaction.response.edit_message(
            embed=embed,
            attachments=[file],
            view=self
        )


        try:
            os.remove(image)
        except:
            pass


    @discord.ui.button(
        label="Hit",
        style=discord.ButtonStyle.success
    )
    async def hit(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "This is not your game.",
                ephemeral=True
            )


        if self.finished:
            return


        self.player_hand.append(
            draw_card(self.deck)
        )


        if hand_value(self.player_hand) > 21:

            self.finished = True

            await finish_fair_game(
                self.fair["id"],
                "Bust",
                0,
                -self.bet
            )

            self.clear_items()

            return await self.send_result(
                interaction,
                "💥 Bust!",
                0xE74C3C
            )


        await self.send_result(
            interaction,
            "🃏 Blackjack",
            0x2ECC71,
            True
        )

    @discord.ui.button(
        label="Stand",
        style=discord.ButtonStyle.primary
    )
    async def stand(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "This is not your game.",
                ephemeral=True
            )


        if self.finished:
            return


        self.finished = True


        dealer_play(
            self.deck,
            self.dealer_hand
        )


        result = compare(
            self.player_hand,
            self.dealer_hand
        )


        if result == "win":

            winnings = self.bet * 2

            await add_balance(
                self.ctx.author.id,
                winnings
            )


            await finish_fair_game(
                self.fair["id"],
                "Win",
                winnings,
                self.bet
            )


            title = "🎉 Blackjack - You Win"
            colour = 0x2ECC71


        elif result == "push":

            await add_balance(
                self.ctx.author.id,
                self.bet
            )


            await finish_fair_game(
                self.fair["id"],
                "Push",
                self.bet,
                0
            )


            title = "🤝 Blackjack - Push"
            colour = 0xF1C40F


        else:

            await finish_fair_game(
                self.fair["id"],
                "Lose",
                0,
                -self.bet
            )


            title = "❌ Blackjack - You Lose"
            colour = 0xE74C3C


        self.clear_items()


        await self.send_result(
            interaction,
            title,
            colour,
            False
        )

class Blackjack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="blackjack",
        aliases=["bj"]
    )
    async def blackjack(
        self,
        ctx,
        amount: float
    ):

        if amount <= 0:
            return await ctx.reply(
                "Invalid bet amount."
            )


        balance = await get_balance(
            ctx.author.id
        )


        if balance < amount:
            return await ctx.reply(
                "You don't have enough balance."
            )


        fair = await create_fair_game(
            ctx.author.id,
            "blackjack",
            amount
        )


        await remove_balance(
            ctx.author.id,
            amount
        )

        await add_wager(
            ctx.author.id,
            amount
        )


        deck = create_deck()


        player_hand = [
            draw_card(deck),
            draw_card(deck)
        ]


        dealer_hand = [
            draw_card(deck),
            draw_card(deck)
        ]


        if is_blackjack(player_hand):

            winnings = amount * 2.5


            await add_balance(
                ctx.author.id,
                winnings
            )


            await finish_fair_game(
                fair["id"],
                "Blackjack",
                winnings,
                winnings - amount
            )


            image = create_blackjack_image(
                player_hand,
                dealer_hand,
                False
            )


            file = discord.File(
                image,
                filename="blackjack.png"
            )


            embed = discord.Embed(
                title="🃏 Natural Blackjack!",
                colour=0x2ECC71
            )


            embed.description = (
                f"{GREEN_COIN} Bet: `{amount:,.2f}`\n"
                f"{GREEN_COIN} Won: `{winnings:,.2f}`"
            )


            embed.set_image(
                url="attachment://blackjack.png"
            )


            await ctx.reply(
                embed=embed,
                file=file
            )


            try:
                os.remove(image)
            except:
                pass


            return



        view = BlackjackView(
            ctx,
            fair,
            deck,
            player_hand,
            dealer_hand,
            amount
        )


        image = create_blackjack_image(
            player_hand,
            dealer_hand,
            True
        )


        file = discord.File(
            image,
            filename="blackjack.png"
        )


        embed = discord.Embed(
            title="🃏 Blackjack",
            colour=0x2ECC71
        )


        embed.description = (
            f"{GREEN_COIN} Bet: `{amount:,.2f}`\n\n"
            f"Player: `{hand_value(player_hand)}`\n"
            f"Dealer: `?`"
        )


        embed.set_image(
            url="attachment://blackjack.png"
        )


        await ctx.reply(
            embed=embed,
            file=file,
            view=view
        )


        try:
            os.remove(image)
        except:
            pass



async def setup(bot):

    await bot.add_cog(
        Blackjack(bot)
    )

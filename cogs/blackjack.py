import discord
from discord.ext import commands
import asyncio
import os

from services.economy import (
    get_balance,
    remove_balance,
    add_balance
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
        cog,
        ctx,
        fair,
        deck,
        player_hand,
        dealer_hand,
        bet
    ):

        super().__init__(timeout=120)

        self.cog = cog
        self.ctx = ctx
        self.fair = fair

        self.deck = deck

        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

        self.bet = bet

        self.finished = False


    async def update_message(
        self,
        interaction,
        hide_dealer=True,
        title="🃏 Blackjack",
        colour=0x2ECC71
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
            f"{GREEN_COIN} **Bet:** "
            f"`£{self.bet:,.2f}`\n\n"

            f"**Your Hand:** "
            f"`{hand_value(self.player_hand)}`\n"

            f"**Dealer:** "
            f"`{'?' if hide_dealer else hand_value(self.dealer_hand)}`"
        )

        embed.set_image(
            url="attachment://blackjack.png"
        )

        embed.add_field(
            name="Provably Fair",
            value=(
                f"Game ID: `{self.fair['id']}`\n"
                f"Verify: `.verify {self.fair['id']}`"
            ),
            inline=False
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
        style=discord.ButtonStyle.success,
        row=0
    )
        async def hit(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "This isn't your game.",
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

            await self.update_message(
                interaction,
                hide_dealer=False,
                title="💥 Bust!",
                colour=0xE74C3C
            )

            return

        await self.update_message(
            interaction
        )


    @discord.ui.button(
        label="Stand",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def stand(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "This isn't your game.",
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

        self.clear_items()

        if result == "win":

            winnings = self.bet * 2
            profit = self.bet

            await add_balance(
                self.ctx.author.id,
                winnings
            )

            await finish_fair_game(
                self.fair["id"],
                "Win",
                winnings,
                profit
            )

            title = "🎉 You Win!"
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

            title = "🤝 Push"
            colour = 0xF1C40F

        else:

            await finish_fair_game(
                self.fair["id"],
                "Lose",
                0,
                -self.bet
            )

            title = "❌ You Lose"
            colour = 0xE74C3C

        await self.update_message(
            interaction,
            hide_dealer=False,
            title=title,
            colour=colour
        )
      class Blackjack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
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
                "You don't have enough points."
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

        deck = create_deck()

        player_hand = [
            draw_card(deck),
            draw_card(deck)
        ]

        dealer_hand = [
            draw_card(deck),
            draw_card(deck)
        ]

        # Natural Blackjack
        if is_blackjack(player_hand):

            winnings = amount * 2.5
            profit = winnings - amount

            await add_balance(
                ctx.author.id,
                winnings
            )

            await finish_fair_game(
                fair["id"],
                "Blackjack",
                winnings,
                profit
            )

            image = create_blackjack_image(
                player_hand,
                dealer_hand,
                hide_dealer=False
            )

            file = discord.File(
                image,
                filename="blackjack.png"
            )

            embed = discord.Embed(
                title="🃏 BLACKJACK!",
                colour=0x2ECC71
            )

            embed.description = (
                f"{GREEN_COIN} **Bet:** `£{amount:,.2f}`\n"
                f"{GREEN_COIN} **Won:** `£{winnings:,.2f}`"
            )

            embed.set_image(
                url="attachment://blackjack.png"
            )

            embed.add_field(
                name="Provably Fair",
                value=f"Game ID: `{fair['id']}`",
                inline=False
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
            self,
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
            hide_dealer=True
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
            f"{GREEN_COIN} **Bet:** `£{amount:,.2f}`\n\n"
            f"**Your Hand:** `{hand_value(player_hand)}`\n"
            f"**Dealer:** `?`"
        )

        embed.set_image(
            url="attachment://blackjack.png"
        )

        embed.add_field(
            name="Provably Fair",
            value=(
                f"Game ID: `{fair['id']}`\n"
                f"Verify: `.verify {fair['id']}`"
            ),
            inline=False
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

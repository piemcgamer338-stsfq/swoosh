import discord
from discord.ext import commands

from database import get_pool

GREEN = "<:Based_GreenCoin:1530472181434155111>"
CHIPS = "<:casino_chips:1530572520506392746>"


class LeaderboardView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=120
        )

    @discord.ui.button(
        label="Daily",
        style=discord.ButtonStyle.success,
        row=0
    )
    async def daily(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        db = await get_pool()

        richest = await db.fetch(
            """
            SELECT discord_id,balance
            FROM users
            ORDER BY balance DESC
            LIMIT 5
            """
        )

        wager = await db.fetch(
            """
            SELECT discord_id,wager
            FROM users
            ORDER BY wager DESC
            LIMIT 5
            """
        )

        embed = discord.Embed(
            title="🏆 Daily Leaderboard",
            colour=0x2ECC71
        )

        balance_text = ""

        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]

        for i,row in enumerate(richest):

            user = interaction.guild.get_member(
                row["discord_id"]
            )

            if user is None:
                continue

            icon = (
                medals[i]
                if i < 3
                else f"{i+1}."
            )

            balance_text += (
                f"{icon} {user.display_name}\n"
                f"{GREEN} `£{row['balance']:,.2f}`\n\n"
            )

        wager_text = ""

        for i,row in enumerate(wager):

            user = interaction.guild.get_member(
                row["discord_id"]
            )

            if user is None:
                continue

            icon = (
                medals[i]
                if i < 3
                else f"{i+1}."
            )

            wager_text += (
                f"{icon} {user.display_name}\n"
                f"{CHIPS} `£{row['wager']:,.2f}`\n\n"
            )

        embed.add_field(
            name=f"{GREEN} Balance",
            value=balance_text or "No Data",
            inline=True
        )

        embed.add_field(
            name=f"{CHIPS} Wagered",
            value=wager_text or "No Data",
            inline=True
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

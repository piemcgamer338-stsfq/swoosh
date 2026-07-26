import discord


class ConfirmButtons(discord.ui.View):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)

        self.value = None


    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.value = True

        await interaction.response.defer()

        self.stop()



    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.value = False

        await interaction.response.defer()

        self.stop()



class ClaimButton(discord.ui.View):

    def __init__(self, user_id, timeout=60):
        super().__init__(timeout=timeout)

        self.user_id = user_id


    @discord.ui.button(
        label="Claim",
        style=discord.ButtonStyle.green
    )
    async def claim(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.user_id:

            return await interaction.response.send_message(
                "❌ This is not your claim button.",
                ephemeral=True
            )


        await interaction.response.send_message(
            "✅ Claimed successfully!",
            ephemeral=True
        )

        self.stop()



class RankClaimButton(discord.ui.View):

    def __init__(self, role_id, timeout=60):
        super().__init__(timeout=timeout)

        self.role_id = role_id


    @discord.ui.button(
        label="Claim Rank",
        style=discord.ButtonStyle.blurple
    )
    async def rank(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        role = interaction.guild.get_role(
            self.role_id
        )

        if role:

            await interaction.user.add_roles(role)

            await interaction.response.send_message(
                "🏆 Rank role claimed!",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ Rank role not found.",
                ephemeral=True
            )

        self.stop()

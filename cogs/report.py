import discord

from discord.ext import commands

from datetime import timedelta

from utils.report_ai import analyse_message


class Report(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="report")
    async def report(self, ctx):

        if ctx.message.reference is None:

            return await ctx.reply(
                "Reply to a message and use `.report`."
            )


        try:

            reported_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )

        except Exception:

            return await ctx.reply(
                "Couldn't fetch that message."
            )


        result = analyse_message(
            reported_message.content
        )


        if not result["violation"]:

            embed = discord.Embed(
                title="🔍 Moderation Analysis",
                colour=0x2ECC71,
                description=(
                    "Analysis determined this message "
                    "does not violate moderation policies or rules."
                )
            )

            embed.add_field(
                name="Status",
                value="✅ No Violation",
                inline=False
            )

            return await ctx.reply(
                embed=embed
            )


        try:

            await reported_message.delete()

        except Exception:
            pass


        try:

            await reported_message.author.timeout(
                timedelta(minutes=10),
                reason="Automatic begging detection"
            )

            action = (
                "Message deleted\n"
                "User timed out for 10 minutes."
            )

        except Exception:

            action = (
                "Message deleted.\n"
                "Couldn't timeout user "
                "(missing permissions)."
            )


        embed = discord.Embed(
            title="🔍 Moderation Analysis",
            colour=0xE74C3C
        )

        embed.add_field(
            name="Status",
            value="❌ Policy Violation Detected",
            inline=False
        )

        embed.add_field(
            name="Category",
            value=result["category"],
            inline=True
        )

        embed.add_field(
            name="Reason",
            value=result["reason"],
            inline=False
        )

        embed.add_field(
            name="Action Taken",
            value=action,
            inline=False
        )

        await ctx.reply(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Report(bot)
    )

import discord

from discord.ext import commands

from database import get_db


class Verify(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.command(
        name="verify"
    )
    async def verify(
        self,
        ctx,
        game_id: str
    ):

        db = await get_db()


        game = await db.fetch_one(
            """
            SELECT *
            FROM game_history
            WHERE id = $1
            """,
            game_id
        )


        if not game:

            return await ctx.reply(
                "Game not found."
            )


        game = dict(game)


        embed = discord.Embed(
            title="Provably Fair Verification",
            colour=0x3498DB
        )


        embed.add_field(
            name="Game",
            value=f"`{game['game_type']}`",
            inline=True
        )


        embed.add_field(
            name="Game ID",
            value=f"`{game['id']}`",
            inline=True
        )


        embed.add_field(
            name="Server Seed Hash",
            value=f"`{game['server_seed_hash']}`",
            inline=False
        )


        embed.add_field(
            name="Server Seed",
            value=f"`{game['server_seed']}`",
            inline=False
        )


        embed.add_field(
            name="Client Seed",
            value=f"`{game['client_seed']}`",
            inline=False
        )


        embed.add_field(
            name="Nonce",
            value=f"`{game['nonce']}`",
            inline=True
        )


        embed.add_field(
            name="Result",
            value=f"`{game['result']}`",
            inline=True
        )


        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )


        await ctx.reply(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Verify(bot)
    )

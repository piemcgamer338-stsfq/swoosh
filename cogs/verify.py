import discord

from discord.ext import commands

from database import get_pool



class Verify(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot



    @commands.command(
        name="verify"
    )
    async def verify(
        self,
        ctx,
        game_id: int
    ):


        pool = await get_pool()


        async with pool.acquire() as conn:


            game = await conn.fetchrow(
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


        embed = discord.Embed(
            title="Provably Fair Verification",
            colour=0x3498DB
        )


        embed.add_field(
            name="Game",
            value=f"`{game['game']}`",
            inline=True
        )


        embed.add_field(
            name="Game ID",
            value=f"`{game['id']}`",
            inline=True
        )


        embed.add_field(
            name="Bet",
            value=f"`{game['bet']:,.2f}`",
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


        embed.add_field(
            name="Multiplier",
            value=f"`{game['multiplier']}x`",
            inline=True
        )


        embed.add_field(
            name="Profit",
            value=f"`{game['profit']:,.2f}`",
            inline=True
        )


        embed.set_footer(
            text="Swoosh Casino • Provably Fair"
        )


        await ctx.reply(
            embed=embed
        )



async def setup(
    bot
):

    await bot.add_cog(
        Verify(bot)
    )

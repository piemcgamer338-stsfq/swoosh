from discord.ext import commands
import discord

from database import get_pool


class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="verify"
    )
    async def verify(self, ctx, game_id: str):

        pool = await get_pool()

        async with pool.acquire() as conn:

            game = await conn.fetchrow(
                """
                SELECT *
                FROM game_history
                WHERE id = $1
                """,
                int(game_id)
            )


        if not game:

            embed = discord.Embed(
                title="Verification Failed",
                description=(
                    "Game ID not found."
                ),
                colour=0xE74C3C
            )

            return await ctx.reply(
                embed=embed
            )


        embed = discord.Embed(
            title="Provably Fair Verification",
            colour=0x2ECC71
        )


        embed.add_field(
            name="Game ID",
            value=f"`#{game['id']}`",
            inline=False
        )


        embed.add_field(
            name="Game",
            value=f"`{game['game']}`",
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


        if "server_seed_hash" in game:

            embed.add_field(
                name="Server Seed Hash",
                value=f"`{game['server_seed_hash']}`",
                inline=False
            )


        if "client_seed" in game:

            embed.add_field(
                name="Client Seed",
                value=f"`{game['client_seed']}`",
                inline=False
            )


        if "nonce" in game:

            embed.add_field(
                name="Nonce",
                value=f"`{game['nonce']}`",
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

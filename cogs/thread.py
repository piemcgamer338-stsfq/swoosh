from discord.ext import commands
import discord

from database import get_pool


class Thread(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="thread",
        invoke_without_command=True
    )
    async def thread(self, ctx):

        await ctx.reply(
            "**Thread Commands**\n"
            "```fix\n"
            ".thread create\n"
            ".thread add @user\n"
            ".thread remove @user\n"
            ".thread delete\n"
            "```"
        )


    @thread.command(name="create")
    async def create(self, ctx):

        thread = await ctx.channel.create_thread(
            name=f"{ctx.author.name}-thread",
            type=discord.ChannelType.private_thread,
            invitable=False
        )

        await thread.add_user(ctx.author)

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO threads(owner_id, thread_id)
                VALUES($1,$2)
                ON CONFLICT DO NOTHING
                """,
                ctx.author.id,
                thread.id
            )

        await thread.send(
            f"👋 Welcome {ctx.author.mention}\n"
            "Staff will assist you shortly."
        )

        await ctx.reply(
            f"✅ Created {thread.mention}"
        )


    @thread.command(name="add")
    async def add(self, ctx, member: discord.Member):

        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.reply(
                "❌ This command can only be used inside a thread."
            )

        await ctx.channel.add_user(member)

        await ctx.reply(
            f"✅ Added {member.mention}"
        )


    @thread.command(name="remove")
    async def remove(self, ctx, member: discord.Member):

        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.reply(
                "❌ This command can only be used inside a thread."
            )

        await ctx.channel.remove_user(member)

        await ctx.reply(
            f"✅ Removed {member.mention}"
        )


    @thread.command(name="delete")
    async def delete(self, ctx):

        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.reply(
                "❌ This command can only be used inside a thread."
            )

        await ctx.reply(
            "🗑️ Deleting thread in 5 seconds..."
        )

        await ctx.channel.delete()


async def setup(bot):
    await bot.add_cog(Thread(bot))

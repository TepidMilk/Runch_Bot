import discord
import asyncio
from discord.ext import commands
from data.graph import HomiePointsGraph

homie = HomiePointsGraph()

class HomiePointCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping homie-cog":
            await msg.channel.send("homie-cog is online...", delete_after=3)

    @commands.command()
    async def add_debt(self, ctx, to_user: discord.Member, points=1):
        homie.add_debt(ctx.author.id, to_user.id, points)
        score = homie.get_score(ctx.author.id, to_user.id)
        await ctx.send(f"{ctx.author.global_name} {score[0]} - {to_user.global_name} {score[1]}")
        
    @commands.command()
    async def settle_debt(self, ctx, to_user: discord.Member, points=0):
        score = homie.get_score(ctx.author.id, to_user.id)
        await ctx.send(f"{to_user.mention},\n Has {ctx.author.global_name} sufficiently paid their Homie Points you (y/n)")

        def check(msg):
            return msg.author == to_user and (msg.content == "y" or msg.content == "n")

        try:
            response = await self.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. The Debt was not settled")

        if response == "y":
            homie.settle_debt(ctx.author.id, to_user.id, points)
            await ctx.send(f"{ctx.author.global_name} {score[0]} - {to_user.global_name} {score[1]}")
            settlement = await ctx.send(f"{ctx.author.global_name} has settled their debt of {points} homie points to {to_user.global_name}")
            await settlement.add_reaction("🤝")
        elif response == "n":
            await ctx.send("The Debt has not been settled.")
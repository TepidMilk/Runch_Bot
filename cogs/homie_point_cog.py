import discord
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
        
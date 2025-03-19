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
    async def give_points(self, ctx, to_user: discord.Member, points=1):
        homie.add_debt(ctx.author, to_user, points)
        score = homie.get_score(ctx.author, to_user)
        await ctx.send(f"{ctx.author.global_name} {score[0]} - {to_user.global_name} {score[1]}")
        
    @commands.command()
    async def settle_debt(self, ctx, to_user: discord.Member, points=0):
        await ctx.send(f"{to_user.mention},\n Has {ctx.author.global_name} sufficiently paid their Homie Points you (y/n)")

        def check(msg):
            return msg.author.id == to_user.id and (msg.content == "y" or msg.content == "n")

        try:
            response = await self.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. The Debt was not settled")

        if response.content == "y":
            homie.settle_debt(ctx.author, to_user, points)
            score = homie.get_score(ctx.author, to_user)
            await ctx.send(f"{ctx.author.global_name} {score[0]} - {to_user.global_name} {score[1]}")
            if points == 0:
                settlement = await ctx.send(f"{ctx.author.global_name} has settled their debt with {to_user.global_name}")
            else:
                settlement = await ctx.send(f"{ctx.author.global_name} has settled their debt of {points} homie points to {to_user.global_name}")
            await settlement.add_reaction("🤝")
        elif response.content == "n":
            await ctx.send("The Debt has not been settled.")

    @commands.command()
    async def list_owed(self, ctx):
        owed_embed = discord.Embed()
        owed_embed.set_author(name=f"{ctx.author.global_name}", icon_url=ctx.author.display_avatar.url)
        owed_embed.add_field(name=f"Total: {homie.get_total_owed(ctx.author)}", value="", inline=False)
        value = []
        for user in homie.graph:
            if ctx.author in homie.graph[user]:
                value.append(f"{user.global_name}: {homie.graph[user][ctx.author]}")
        owed_embed.add_field(name="", value="\n".join(value), inline=False)
        await ctx.send(embed=owed_embed)

    @commands.command()
    async def list_debt(self, ctx):
        debt_embed = discord.Embed(title=None)
        debt_embed.set_author(name=f"{ctx.author.global_name}'s Debts", icon_url=ctx.author.display_avatar.url)
        debts = homie.get_debt(ctx.author)
        value = []
        for user in debts:
            value.append(f"{user.global_name}: {debts[user]}")
        debt_embed.add_field(name="", value="\n".join(value), inline=False)
        await ctx.send(embed=debt_embed)
    
            
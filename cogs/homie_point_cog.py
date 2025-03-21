import discord
import asyncio
import pickle
from discord.ext import commands
from data.graph import HomiePointsGraph

def is_channel(ctx):
    return (ctx.channel.id == 1108568875102113792 or ctx.channel.id == 1351608689550688328)

def save(data, filename="homie.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(data, file)

def load(filename="homie.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return HomiePointsGraph()

homie = HomiePointsGraph()

class HomiePointCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping homie-cog":
            await msg.channel.send("homie-cog is online...", delete_after=3)

    @commands.command()
    @commands.check(is_channel)
    async def give_points(self, ctx, to_user: discord.Member, points=1):
        homie.add_debt(ctx.author.id, to_user.id, points)
        save(homie)
        score = homie.get_score(ctx.author.id, to_user.id)
        await ctx.send(f"{ctx.author.global_name} {score[1]} - {to_user.global_name} {score[0]}")
        
    @commands.command()
    @commands.check(is_channel)
    async def settle_debt(self, ctx, to_user: discord.Member, points=0):
        await ctx.send(f"{to_user.mention},\n Has {ctx.author.global_name} sufficiently paid their Homie Points you (y/n)")

        def check(msg):
            return msg.author.id == to_user.id and (msg.content == "y" or msg.content == "n")

        try:
            response = await self.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. The Debt was not settled")

        if response.content == "y":
            homie.settle_debt(ctx.author.id, to_user.id, points)
            save(homie)
            score = homie.get_score(ctx.author.id, to_user.id)
            await ctx.send(f"{ctx.author.global_name} {score[0]} - {to_user.global_name} {score[1]}")
            if points == 0:
                settlement = await ctx.send(f"{ctx.author.global_name} has settled their debt with {to_user.global_name}")
            else:
                settlement = await ctx.send(f"{ctx.author.global_name} has settled their debt of {points} homie points to {to_user.global_name}")
            await settlement.add_reaction("🤝")
        elif response.content == "n":
            await ctx.send("The Debt has not been settled.")

    @commands.command()
    @commands.check(is_channel)
    async def list_owed(self, ctx):
        owed_embed = discord.Embed()
        owed_embed.set_author(name=f"{ctx.author.global_name}", icon_url=ctx.author.display_avatar.url)
        owed_embed.add_field(name=f"Total: {homie.get_total_owed(ctx.autho.idr)}", value="", inline=False)
        value = []
        for id in homie.graph:
            user = self.bot.get_user(id)
            if ctx.author.id in homie.graph[id]:
                value.append(f"{user.global_name}: {homie.graph[id][ctx.author.id]}")
        owed_embed.add_field(name="", value="\n".join(value), inline=False)
        await ctx.send(embed=owed_embed)

    @commands.command()
    @commands.check(is_channel)
    async def list_debts(self, ctx):
        debt_embed = discord.Embed(title=None)
        debt_embed.set_author(name=f"{ctx.author.global_name}'s Debts", icon_url=ctx.author.display_avatar.url)
        debts = homie.get_debt(ctx.author.id)
        value = []
        for id in debts:
            user = self.bot.get_user(id)
            value.append(f"{user.global_name}: {debts[id]}")
        debt_embed.add_field(name="", value="\n".join(value), inline=False)
        await ctx.send(embed=debt_embed)


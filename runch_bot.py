import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.homie_point_cog import HomiePointCog

#Load token from .env
load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

#set bot intents. Allows messages, reactions, access to member info and emojis and stickers
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.emojis_and_stickers = True
bot = commands.Bot(command_prefix="!", intents=intents)

def is_me(ctx):
    return ctx.author.id == 182681120314228736

@bot.event
async def on_ready():
    print("Bot is online...")
    print(f"Logged in as {bot.user}...")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
@commands.check(is_me)
async def unloadHomie(ctx):
    await bot.remove_cog("AlertCog")

@bot.command()
@commands.check(is_me)
async def reloadHomie(ctx):
    await bot.add_cog(HomiePointCog(bot))

async def startcog():
    await bot.add_cog(HomiePointCog(bot))

asyncio.run(startcog())
bot.run(TOKEN)

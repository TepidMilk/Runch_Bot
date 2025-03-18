import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

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

@bot.event
async def on_ready():
    print("Bot is online...")
    print(f"Logged in as {bot.user}...")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

bot.run(TOKEN)

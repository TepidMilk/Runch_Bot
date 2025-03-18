import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents(message_content=True, reactions=True, members=True, emojis_and_stickers=True)

client = discord.Client(intents=intents)


import discord
import asyncio
from discord.ext import commands
from data.movie_list import MovieList

movies = MovieList()

def is_channel(ctx):
    return (ctx.channel.id == 1346252701159129328 or ctx.channel.id == 1351608689550688328)

class MovieListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping movie-cog":
            await msg.channel.send("movie-cog is online...", delete_after=3)
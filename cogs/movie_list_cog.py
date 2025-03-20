import discord
import asyncio
from discord.ext import commands
from data.movie_list import MovieList
import random

movies_list = MovieList()

def is_channel(ctx):
    return (ctx.channel.id == 1346252701159129328 or ctx.channel.id == 1351608689550688328)

class MovieListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping movie-cog":
            await msg.channel.send("movie-cog is online...", delete_after=3)

    @commands.command()
    @commands.check(is_channel)
    async def add_movie(self, ctx, movie):
        movies_list.add_movie(ctx.author, movie)
        await ctx.send(f"{ctx.author.global_name} added {movie} to their list")

    @commands.command()
    @commands.check(is_channel)
    async def remove_movie(self, ctx, movie):
        movies_list.remove_movie(ctx.author, movie)
        await ctx.send(f"{ctx.author.global_name} removed {movie} from their list")

    @commands.command()
    @commands.check(is_channel)
    async def list_movies(self, ctx):
        list_embed = discord.Embed()
        list_embed.set_author(name=f"{ctx.author.global_name}'s Movie List", icon_url=ctx.author.display_avatar.url)
        list_embed.add_field(name="", value="\n".join(movies_list.get_movie_list(ctx.author)), inline=False)
        await ctx.send(embed=list_embed)

    @commands.command()
    @commands.check(is_channel)
    async def list_all_movies(self, ctx):
        list_embed = discord.Embed()
        list_embed.set_author(name="Movie List", icon_url=self.bot.user.display_avatar.url)
        list_embed.add_field(name="", value="\n".join(movies_list.get_all_movies()), inline=False)
        await ctx.send(embed=list_embed)

    @commands.command()
    @commands.check(is_channel)
    async def movie_poll(self, ctx):
        movie_poll = discord.Poll(question="Vote for your Favorite Movie!", duration=1)
        for user in movies_list.movies:
            answer = random.choice(movies_list.movies[user])
            movie_poll.add_answer(str(answer))
        await ctx.send(poll=movie_poll)



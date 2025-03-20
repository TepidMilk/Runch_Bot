import discord
import asyncio
import pickle
import os
from discord.ext import commands, tasks
from data.movie_list import MovieList
import random

def save_movie_list(movies, filename="movie_data.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(movies, file)

def load_movie_list(filename="movie_data.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
    return MovieList()

def is_channel(ctx):
    return (ctx.channel.id == 1346252701159129328 or ctx.channel.id == 1351608689550688328)

class MovieListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.movies = load_movie_list()

    def save_movies(self):
        save_movie_list(self.movies)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping movie-cog":
            await msg.channel.send("movie-cog is online...", delete_after=3)

    @commands.command()
    @commands.check(is_channel)
    async def add_movie(self, ctx, movie):
        msg = self.movies.add_movie(ctx.author, movie)
        self.save_movies()
        if msg == None:
            await ctx.send(f"{ctx.author.global_name} added {movie} to their list")
        else:
            await ctx.send(msg)

    @commands.command()
    @commands.check(is_channel)
    async def remove_movie(self, ctx):
        self.movies.remove_movie(ctx.author)
        self.save_movies()
        await ctx.send(f"{ctx.author.global_name} removed their movie")

    @commands.command()
    @commands.check(is_channel)
    async def list_movies(self, ctx):
        list_embed = discord.Embed()
        list_embed.set_author(name="The Kingdom's Movie List", icon_url=self.bot.user.display_avatar.url)
        list_embed.add_field(name="\n".join(self.movies.get_all_movies()), value="", inline=False)
        await ctx.send(embed=list_embed)

    @commands.command()
    @commands.check(is_channel)
    async def movie_poll(self, ctx):
        movie_poll = discord.Poll(question="Vote for your Favorite Movie!", duration=1)
        for user in self.movies.movies:
            answer = random.choice(self.movies.movies[user])
            movie_poll.add_answer(str(answer))
        await ctx.send(poll=movie_poll)



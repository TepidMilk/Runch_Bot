import discord
import asyncio
import os
import pickle
import datetime
from discord.ext import commands, tasks
from data.movie_list import MovieList
import random

def is_channel(ctx):
    return (ctx.channel.id == 1346252701159129328 or ctx.channel.id == 1351608689550688328)

def save(data, filename="movie_list.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(data, file)

def load(filename="movie_list.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return MovieList()

movie_list = load()

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
        msg = movie_list.add_movie(ctx.author.id, movie)
        save(movie_list)
        if msg == None:
            await ctx.send(f"{ctx.author.global_name} added {movie} to the list")
        else:
            await ctx.send(msg)

    @commands.command()
    @commands.check(is_channel)
    async def remove_movie(self, ctx):
        movie_list.remove_movie(ctx.author.id)
        save(movie_list)
        await ctx.send(f"{ctx.author.global_name} removed their movie")
        

    @commands.command()
    @commands.check(is_channel)
    async def list_movies(self, ctx):
        list_embed = discord.Embed()
        list_embed.set_author(name="The Kingdom's Movie List", icon_url=self.bot.user.display_avatar.url)
        list_embed.add_field(name="\n".join(movie_list.get_all_movies(self.bot)), value="", inline=False)
        await ctx.send(embed=list_embed)

    @commands.command()
    @commands.check(is_channel)
    async def movie_poll(self, ctx):
        duration = datetime.timedelta(hours=1)
        movie_poll = discord.Poll(question="Movie Sundays", duration=duration)
        for answer in movie_list.get_all_movies(self.bot):
            movie_poll.add_answer(text=answer)
        await ctx.send(poll=movie_poll)
        movie_list.reset_list()
        save(movie_list)
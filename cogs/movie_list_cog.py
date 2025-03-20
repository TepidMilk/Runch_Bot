import discord
import asyncio
import os
from discord.ext import commands, tasks
from data.movie_list import MovieList
import random

def is_channel(ctx):
    return (ctx.channel.id == 1346252701159129328 or ctx.channel.id == 1351608689550688328)

movie_list = MovieList()

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
        msg = movie_list.add_movie(ctx.author, movie)
        if msg == None:
            await ctx.send(f"{ctx.author.global_name} added {movie} to their list")
        else:
            await ctx.send(msg)

    @commands.command()
    @commands.check(is_channel)
    async def remove_movie(self, ctx):
        movie_list.remove_movie(ctx.author)
        await ctx.send(f"{ctx.author.global_name} removed their movie")
        

    @commands.command()
    @commands.check(is_channel)
    async def list_movies(self, ctx):
        list_embed = discord.Embed()
        list_embed.set_author(name="The Kingdom's Movie List", icon_url=self.bot.user.display_avatar.url)
        list_embed.add_field(name="\n".join(movie_list.get_all_movies()), value="", inline=False)
        await ctx.send(embed=list_embed)

    @commands.command()
    @commands.check(is_channel)
    async def movie_poll(self, ctx):
        movie_poll = discord.Poll(question="Vote for your Favorite Movie!", duration=1)
        for user in movie_list.movies:
            answer = random.choice(self.movies.movies[user])
            movie_poll.add_answer(str(answer))
        await ctx.send(poll=movie_poll)

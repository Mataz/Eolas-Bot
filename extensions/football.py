import random
import discord
from discord.ext import commands as eolas


class Football:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?cavani - Print a random gif of Cavani.
        @eolas.command()
        async def cavani():
            cavani_gifs = [
                "https://media.giphy.com/media/3oKGzl8zDsyKif2xdS/giphy.gif",
                "https://media.giphy.com/media/3oKGzi31QTqbppVOjS/giphy.gif",
                "https://media.giphy.com/media/l4FsydT8HX6EWau9a/giphy.gif",
                "https://media.giphy.com/media/AAvqQob2BUFCo/giphy.gif",
                "https://media.giphy.com/media/l1J3Qcd7OmaqfnXQ4/giphy.gif"]

            rand_gif = random.choice(cavani_gifs)

            await eolas.say(rand_gif)


def setup(eolas):
    eolas.add_cog(Football(eolas))

import random
import discord
from discord.ext import commands as eolas


class Games:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?chess - Print a link of a randomly selected puzzle from Lichess.org
        @eolas.command()
        async def chess():
            random_number = random.sample(range(1, 125000), 1)
            random_ID = ("".join(map(str, random_number)))
            puzzle_link = f'https://lichess.org/training/{("".join(map(str, random_number)))}'
            print('Lichess Puzzle ID:' + '\n' + random_ID + '\n')
            await eolas.say('Lichess Puzzle:' + '\n' + puzzle_link)


def setup(eolas):
    eolas.add_cog(Games(eolas))

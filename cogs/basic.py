import bs4
import random
import requests

import discord
from discord.ext import commands

class BasicCog(commands.Cog, name="Basic Commands"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def facts(self, ctx):
        """Scrape unkno.com and return the fact from it."""
        source = requests.get('http://unkno.com/').text
        soup = bs4.BeautifulSoup(source, 'lxml')
        # facts = soup.find('section', class_='body')
        fact = soup.find('div', id='content')
        print(fact.text)
        await ctx.send('Here is your fact: ' + '\n' + fact.text)

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)
    
    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as e:
            await ctx.send('Format has to be in NdN!')

        result = ', '.join(
            str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))
    # TODO: Do a max limit to avoid spam
    @commands.command()
    async def repeat(self, ctx, times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await ctx.send(content)


    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

def setup(bot):
    bot.add_cog(BasicCog(bot))
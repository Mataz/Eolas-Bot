import discord
from discord.ext import commands
import random
import aiohttp
from bs4 import BeautifulSoup

eolas = commands.Bot(command_prefix="?")


@eolas.event
async def on_ready():
    print('Logged in as')
    print(eolas.user.name)
    print(eolas.user.id)
    print('------')


@eolas.command()
async def coinflip(ctx):
    """
    ?coinflip - Flip a coin and choose "Pile" or "Face".
    """
    choices = ('Pile !', 'Face !')
    await ctx.send(random.choice(choices))


@eolas.command()
async def add(left : int, right : int):
    """
    Adds two number together.
    """
    await eolas.say(left + right)


@eolas.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@eolas.command()
async def facts(ctx):
    """
    ?facts - A command that will provide a random fact.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.unkno.com') as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            facts = soup.find('div', attrs={'id': 'content'})

            for fact in facts:
                fact = fact.strip()
                await ctx.send(fact)


@eolas.event
async def on_message(message):
    if message.content == "Yo":
        await eolas.send_message(message.channel, "Salut !")


eolas.run('token')

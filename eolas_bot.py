import discord
import random
import aiohttp
import bs4
import requests
from discord.ext import commands

client = discord.Client()

description = '''There are a number of utility commands being showcased here.'''
eolas = commands.Bot(command_prefix='?', description=description)

hello_list = ['Yo', 'yo', 'Hey', 'hey', 'Salut', 'salut', 'Bonjour', 'bonjour']
foot_list = ['Neymar', 'neymar','Cavani', 'cavani', 'PSG', 'psg',
             'Zidane', 'zidane', 'Real', 'real', 'Madrid', 'madrid'
             'Barca', 'barca', 'OM', 'Deschamps', 'deschamps', 'Blaise',
             'blaise']

# choices = (
#     'https://media.giphy.com/media/hBO3iUfEtI2s0/giphy.gif'
#     'https://media.giphy.com/media/TEBouaNRv736E/giphy.gif'
#     'https://media.giphy.com/media/lXB3CaZsXkyf6/giphy.gif'
#     'https://media.giphy.com/media/i1JSXl0MfeRd6/giphy.gif'
# )


@eolas.event
async def on_member_join(member):
    server = member.server
    fmt = 'Bienvenue {0.mention} chez {1.name} !'
    await eolas.send_message(server, fmt.format(member, server))


@eolas.event
async def on_ready():
    print('Logged in as')
    print(eolas.user.name)
    print(eolas.user.id)
    print('------')


@eolas.event
async def on_message(message):
    if message.content in hello_list:
        await eolas.send_message(message.channel, "Salut !")
    if any(i in message.content for i in foot_list):
        await eolas.send_message(message.channel, 'https://media.giphy.com/media/hBO3iUfEtI2s0/giphy.gif')
        await eolas.send_message(message.channel, "Non, pas de ça ici, s'il-vous-plaît.")
    await eolas.process_commands(message)


# ?news - Scrape a specific block on lemonde.fr and return the news from it.
@eolas.command()
async def news():
    source = requests.get('http://www.lemonde.fr/').text
    soup = bs4.BeautifulSoup(source, 'lxml')
    bloc = soup.find('ul', class_='liste_horaire')
    for news_lm in bloc.find_all('li'):

        hours = news_lm.span.text
        print(hours)

        try:
            links = news_lm.find('a')['href']
            lm_link = f'https://www.lemonde.fr/{links}'
        except Exception as e:
            lm_link = None

        print(lm_link)
        print()
        if lm_link is not None:
            await eolas.say(hours + "\n" + lm_link)
        else:
            pass


@eolas.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await eolas.say(left + right)


@eolas.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await eolas.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await eolas.say(result)


@eolas.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await eolas.say(random.choice(choices))


@eolas.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await eolas.say(content)


@eolas.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await eolas.say('{0.name} joined in {0.joined_at}'.format(member))


@eolas.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await eolas.say('No, {0.subcommand_passed} is not cool'.format(ctx))


# TODO : facts doesn't work, get on it
# @eolas.command()
# async def facts():
#     """
#     ?facts - A command that will provide a random fact.
#     """
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://www.lemonde.fr/') as response:
#             soup = BeautifulSoup(await response.text(), 'lxml')
#             news = soup.select('div[class="titres clearfix"]')
#
#             for i in news:
#                 i = news.strip()
#                 await eolas.send(i)


eolas.run('Mzc2MDc1MDU3MjA3NzA1NjAw.DOIGfA.bYRke2_k2eMz7p9UU_kOsN9Ea7Y')

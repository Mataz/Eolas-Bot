import discord
import random
import aiohttp
import bs4
import requests
import csv
import os.path
import pyowm
from discord.ext import commands


description = '''There are a number of utility commands being showcased here.'''
eolas = commands.Bot(command_prefix='?', description=description)

hello_list = ['Yo', 'yo', 'Hey', 'hey', 'Salut', 'salut', 'Bonjour', 'bonjour']
foot_list = ['Neymar', 'neymar','Cavani', 'cavani', 'PSG', 'psg',
             'Zidane', 'zidane', 'Real', 'real', 'Madrid', 'madrid'
             'Barca', 'barca', 'OM', 'Deschamps', 'deschamps', 'Blaise',
             'blaise']


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
            titles = news_lm.find('a').text
        except Exception as e:
            titles = None

        print(titles)

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

        filename = 'PATH.csv'
        fileEmpty = os.stat(filename).st_size == 0

        with open(filename, 'a') as csv_file:
            headers = ['Hours', 'Titles', 'Links']

            csv_writer = csv.DictWriter(csv_file, fieldnames=headers,
                                        delimiter='\t')
            if fileEmpty:
                csv_writer.writeheader()  # file doesn't exist, write header
            csv_writer.writerow(
                {'Hours': hours, 'Titles': titles, 'Links': lm_link})

        csv_file.close()  


# ?facts - Scrape unkno.com and return the fact from it.
@eolas.command()
async def facts():
    source = requests.get('http://unkno.com/').text
    soup = bs4.BeautifulSoup(source, 'lxml')
    # facts = soup.find('section', class_='body')
    fact = soup.find('div', id='content')
    print(fact.text)
    await eolas.say('Here is your fact: ' + '\n' + fact.text)        

    
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


# ?chess - Print a link of a randomly selected puzzle from Lichess.org
@eolas.command()
async def chess():
    random_number = random.sample(range(1, 125000), 1)
    random_ID = ("".join(map(str, random_number)))
    puzzle_link = f'https://lichess.org/training/{("".join(map(str, random_number)))}'
    print('Lichess Puzzle ID:' + '\n' + random_ID + '\n')
    await eolas.say('Lichess Puzzle:' + '\n' + puzzle_link)


# ?meteo <location> - Print the forecast of a specific location.
@eolas.command()
async def meteo(*, name):
    owm = pyowm.OWM('OWM_API_KEY', language='fr')

    observation = owm.weather_at_place(name)
    weather = observation.get_weather()
    location = observation.get_location()
    get_temperature = weather.get_temperature(unit='celsius')
    get_wind = weather.get_wind()

    await eolas.say('Lieu: {}'.format(location.get_name()))
    await eolas.say('Température: {}'.format(get_temperature['temp']) + u'\N{DEGREE SIGN}C')
    await eolas.say('Vitesse du vent: {}'.format(get_wind['speed']) + ' m/s')
    await eolas.say('Description: {}'.format(weather.get_detailed_status()))


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
    
    
eolas.run('BOT_TOKEN')

import random
import bs4
import requests
import discord
from discord.ext import commands as eolas


class Basic:
    def __init__(self, eolas):
        self.eolas = eolas

        @eolas.event
        async def on_member_join(member):
            server = member.server
            fmt = 'Bienvenue {0.mention} chez {1.name} !'
            await eolas.send_message(server, fmt.format(member, server))

        @eolas.event
        async def on_message(message):

            hello_list = ['Yo', 'yo', 'Hey', 'hey', 'Salut', 'salut',
                          'Bonjour', 'bonjour']
            foot_list = ['Neymar', 'neymar', 'PSG', 'psg', 'Zidane', 'zidane',
                         'Barca', 'barca', 'OM', 'Deschamps', 'deschamps',
                         'Blaise', 'blaise']

            if message.content in hello_list:
                await eolas.send_message(message.channel, "Salut !")
            if any(i in message.content for i in foot_list):
                await eolas.send_message(message.channel,
                                         'https://media.giphy.com/media/hBO3iUfEtI2s0/giphy.gif')
                await eolas.send_message(message.channel,
                                         "Non, pas de ça ici, s'il-vous-plaît.")
            await eolas.process_commands(message)
        
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

            result = ', '.join(
                str(random.randint(1, limit)) for r in range(rolls))
            await eolas.say(result)

        @eolas.command(
            description='For when you wanna settle the score some other way')
        async def choose(*choices: str):
            """Chooses between multiple choices."""
            await eolas.say(random.choice(choices))

        @eolas.command()
        async def repeat(times: int, content='repeating...'):
            """Repeats a message multiple times."""
            for i in range(times):
                await eolas.say(content)

        @eolas.command()
        async def joined(member: discord.Member):
            """Says when a member joined."""
            await eolas.say('{0.name} joined in {0.joined_at}'.format(member))

        @eolas.group(pass_context=True)
        async def cool(ctx):
            """Says if a user is cool.
            In reality this just checks if a subcommand is being invoked.
            """
            if ctx.invoked_subcommand is None:
                await eolas.say(
                    'No, {0.subcommand_passed} is not cool'.format(ctx))


def setup(eolas):
    eolas.add_cog(Basic(eolas))

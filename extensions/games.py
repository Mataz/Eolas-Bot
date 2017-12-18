import random
import discord
import bs4
import requests
from discord.ext import commands as eolas


class Games:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?chess - Print a link of a randomly selected puzzle from Lichess.org
        @eolas.command()
        async def chess():
            """Print a link of a randomly selected puzzle from Lichess.org"""
            random_number = random.sample(range(1, 125000), 1)
            random_ID = ("".join(map(str, random_number)))
            puzzle_link = f'https://lichess.org/training/{("".join(map(str, random_number)))}'
            print('Lichess Puzzle ID:' + '\n' + random_ID + '\n')
            await eolas.say('Lichess Puzzle:' + '\n' + puzzle_link)
            
        # ?gwent - Print the top 5 decks of the week on gwentdb.com
        @eolas.command()
        async def gwent():
            """Print the top 5 decks of the week on gwentdb.com"""
            source = requests.get(
                'http://www.gwentdb.com/decks?filter-deck-time-frame=3').text
            soup = bs4.BeautifulSoup(source, 'lxml')
            
            for hot_decks in soup.find_all('tr', class_='deck-row')[:5]:
                titles = hot_decks.a.text
                print(titles)

                try:
                    links = hot_decks.find('a')['href']
                    gw_link = f'http://www.gwentdb.com/{links}'
                except Exception as e:
                    gw_link = None
                
                print(gw_link)
                print()

                if gw_link is not None:
                    await eolas.say(titles + "\n\n" + gw_link)
                else:
                    pass


def setup(eolas):
    eolas.add_cog(Games(eolas))

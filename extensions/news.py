import bs4
import requests
import csv
import os.path
import discord
from discord.ext import commands as eolas


class News:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?news - Scrape a specific block on lemonde.fr and return the news from it
        @eolas.command()
        async def news():
            """Scrape a specific block on lemonde.fr and return the news from it."""
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
                
        # @space - Scrape the latest news on space.com
        @eolas.command()
        async def space():
            """Scrape the latest news on space.com"""
            source = requests.get('https://www.space.com/news').text
            soup = bs4.BeautifulSoup(source, 'lxml')

            for latest_news in soup.find_all('li', class_='search-item line pure-g')[:5]:
                titles = latest_news.h2.text
                print(titles)

                try:
                    links = latest_news.find('a')['href']
                    space_link = f'https://www.space.com/{links}'
                except Exception as e:
                    space_link = None
                print(space_link)

                summary = latest_news.find('p', class_='mod-copy').text.strip()
                print(summary)

                if space_link is not None:
                    await eolas.say(space_link + '\n')
                else:
                    pass


def setup(eolas):
    eolas.add_cog(News(eolas))

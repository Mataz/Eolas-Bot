import bs4
import requests
import csv
import os.path
import discord
from discord.ext import commands as eolas


class News(eolas.Cog):
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

        # @space - Scrape the latest news on spaceflightnow.com
        @eolas.command()
        async def space():
            """Scrape the latest news on spaceflightnow.com"""
            source = requests.get(
                'https://spaceflightnow.com/category/news-archive/').text
            soup = bs4.BeautifulSoup(source, 'lxml')

            for latest_news in soup.find_all('div', class_='mh-loop-content clearfix')[
                               :3]:

                titles = latest_news.h3.text.strip().upper()
                print(titles)

                try:
                    links = latest_news.find('a')['href']
                except Exception as e:
                    links = None
                print(links + '\n')

                summary = textwrap.fill(
                    latest_news.find('div', class_='mh-excerpt').text.strip(), 60)
                print(summary + '\n' * 2)

                if links is not None:
                    await eolas.say(titles + '\n' + links + '\n\n' + summary + '\n' *2 + '_ _')
                else:
                    pass


def setup(eolas):
    eolas.add_cog(News(eolas))

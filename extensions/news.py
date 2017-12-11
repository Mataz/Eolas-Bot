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


def setup(eolas):
    eolas.add_cog(News(eolas))

import random
import discord
import bs4
import requests
from selenium import webdriver
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
        
        # ?hearthstone - Print the current top 3 overperforming decks listed on hsreplay
        @eolas.command()
        async def hearthstone():
            """Print the current top 3 overperforming decks listed on hsreplay"""
            driver = webdriver.Chrome()
            driver.implicitly_wait(15)
            driver.get('https://hsreplay.net/meta/')

            tier_elem = driver.find_elements_by_class_name('tier-header')
            tiers = [x.text for x in tier_elem][:1]

            names_elem = driver.find_elements_by_class_name('archetype-name')
            names = [x.text for x in names_elem][:3]

            percent_elem = driver.find_elements_by_class_name('archetype-data')
            percents = [x.text for x in percent_elem][:3]

            links = [link.get_attribute('href') for link in driver.find_elements_by_xpath(
                '//*[@id="tierlist"]/div/div/div/li/a/div/a')][:3]

            for tier in tiers:
                await eolas.say(str(tier[6:])+ '\n' + '--------------------'
                                                      '----------------------------')
            for name, percent, link in zip(names, percents, links):
                await eolas.say(str(name) + ' > ' + str(percent) + ' winrate ' + ' | ' + str(
                    link) + '\n' + '------------------------------------------------')
            driver.quit()


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

                cards = hot_decks.find('td', class_='col-card-count').text
                print('Cards: ' + cards)

                melee = hot_decks.find('span', class_='melee').text
                ranged = hot_decks.find('span', class_='ranged').text
                siege = hot_decks.find('span', class_='siege').text
                print(
                    'Attack: ' + melee + ' | ' + 'Ranged: ' + ranged + ' | '
                    + 'Siege: ' + siege)

                rating = hot_decks.find('div',
                                        class_='rating-sum rating-average rating-average-ratingPositive').text
                updated = hot_decks.find('td', class_='col-updated').text
                print('Rating: ' + rating + ' | ' + 'Updated: ' + updated)

                total = hot_decks.find('span', class_='power-total').text
                
                if titles is not None:
                    await eolas.say(titles + '\n' * 2
                                    + '<:gwent_card:392317309026304001> '
                                    + cards + ' | '
                                    + '<:gwent_melee:392316109547765763> '
                                    + melee + ' | '
                                    + '<:gwent_ranged:392316253135699970> '
                                    + ranged + ' | '
                                    + '<:gwent_siege:392316109916864512> '
                                    + siege
                                    + ' | ' + '<:sigma:392352438302015488>'
                                    + total + '\n' * 2
                                    + 'Rating: ' + rating + ' | ' + 'Updated: '
                                    + updated + ' |' + '\n'
                                    + '--------------------'
                                      '--------------------'
                                      '--------')
                else:
                    pass
            await eolas.say('http://www.gwentdb.com/decks?filter-deck-time-frame=3')


def setup(eolas):
    eolas.add_cog(Games(eolas))

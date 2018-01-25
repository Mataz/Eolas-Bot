import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table
import discord
from discord.ext import commands as eolas


class Crypto:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?coins - Print the current top 5 coins.
        @eolas.command()
        async def coins():
            """Print the current top 5 coins on coinmarketcap.com"""
            data = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=5').json()

            for currency in data:
                rank = currency['rank']
                name = currency['name']
                price_usd = currency['price_usd']
                market_cap_usd = currency['market_cap_usd']
                split_market_cap = ' '.join(                # Need to work the split
                    market_cap_usd[i:i + 3] for i in range(0, len(market_cap_usd), 3))
                change_24h = currency['percent_change_24h']
                print(
                    rank + ' | ' + name.upper() + ' | ' + '$' + price_usd + ' | ' + '$'
                    + market_cap_usd + ' | ' + change_24h + '%')
                print()
                await eolas.say(rank + ' | ' + name.upper() + ' | ' + '$' + price_usd
                                + ' | ' + '$' + market_cap_usd + ' | ' + change_24h + '%'
                                + '\n' + '_ _') # '_ _' is to create a clean line break on Discord
        
        # ?coinschanges - Print the top 5 changes in the last 24 hrs
        @eolas.command()
        async def coinschanges():
            """Print the top 5 increase (in %) in the last 24 hours."""
            url = 'https://api.coinmarketcap.com/v1/ticker/'
            data = requests.get(url).json()
            channel = discord.Object(id='ID_OF_YOUR_CHANNEL')
            ordered_data = sorted(data, key=lambda k: (float(k['percent_change_24h']),
                                                       (k['percent_change_7d'])), reverse=True)[:5]
            raw_data_increase = {}
            if not os.path.exists('df_image'):
                os.makedirs('df_image')
            os.chdir('df_image')

            for currency in ordered_data:
                rank = currency['rank']
                name = currency['name']
                percent_change_24h = currency['percent_change_24h']
                percent_change_7d = currency['percent_change_7d']
                price_usd = float(currency['price_usd'])
                price_usd = f'{price_usd:.2f}'

                raw_data_increase.setdefault('Rank', [])
                raw_data_increase['Rank'].append(rank)
                raw_data_increase.setdefault('Name', [])
                raw_data_increase['Name'].append(name)
                raw_data_increase.setdefault('Change last 24h (%)', [])
                raw_data_increase['Change last 24h (%)'].append(percent_change_24h)
                raw_data_increase.setdefault('Change last 7d (%)', [])
                raw_data_increase['Change last 7d (%)'].append(percent_change_7d)
                raw_data_increase.setdefault('Price(USD)', [])
                raw_data_increase['Price(USD)'].append(price_usd)
                # print(raw_data)

            df = pd.DataFrame(raw_data_increase,
                              columns=['Rank', 'Name', 'Change last 24h (%)',
                                       'Change last 7d (%)', 'Price(USD)'])

            print(df.to_string(index=False))

            # set fig size
            fig, ax = plt.subplots(figsize=(9.5, 2.7))
            # no axes
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            # no frame
            ax.set_frame_on(False)
            # plot table
            tab = table(ax, df, rowLabels=[''] * df.shape[0], loc='center')
            # set font manually
            tab.auto_set_font_size(False)
            tab.set_fontsize(10)
            # set scale
            tab.scale(1, 2.5)
            # save the result
            plt.savefig('cryptopinc.png')

            await eolas.send_file(channel, 'cryptopinc.png')


def setup(eolas):
    eolas.add_cog(Crypto(eolas))

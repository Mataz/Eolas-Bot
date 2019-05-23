import requests
import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from pandas.tools.plotting import table

import discord
from discord.ext import commands

# TODO: FIX Matplotlib 

class Crypto(commands.Cog, name="Crypto Commands"):
    def __init__(self, bot):
        self.bot = bot

    # ?coins - Print the current top 5 coins.
    @commands.command()
    async def coins(self, ctx):
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
            await ctx.send(rank + ' | ' + name.upper() + ' | ' + '$' + price_usd
                            + ' | ' + '$' + market_cap_usd + ' | ' + change_24h + '%'
                            + '\n' + '_ _') # '_ _' is to create a clean line break on Discord

    # ?coinschanges - Print the top 5 changes in the last 24 hrs
    # @commands.command()
    # async def coinschanges(self, ctx):
    #     """Print the top 5 increase (in %) in the last 24 hours."""
    #     url = 'http://coincap.io/front'

    #     try:
    #         data = requests.get(url).json()
    #     except Exception as e:
    #         data = None

    #     channel = discord.Object(id='ID_OF_YOUR_CHANNEL')
    #     top100_data = sorted(data, key=lambda k: (float(k['mktcap'])), reverse=True)[
    #                     :100]
    #     ordered_data = sorted(top100_data, key=lambda k: (float(k['cap24hrChange'])),
    #                             reverse=True)[:5]
    #     raw_data_increase = {}
    #     if not os.path.exists('df_image'):
    #         os.makedirs('df_image')
    #     os.chdir('df_image')

    #     for currency in ordered_data:
    #         name = currency['long']
    #         market_cap = float(currency['mktcap'])
    #         market_cap_rounded = f'{market_cap:,.2f}'
    #         if data is not None:
    #             percent_change_24 = currency['cap24hrChange']
    #         price = float(currency['price'])
    #         price_rounded = f'{price:.2f}'

    #         raw_data_increase.setdefault('Name', [])
    #         raw_data_increase['Name'].append(name)
    #         raw_data_increase.setdefault('Market Cap(USD)', [])
    #         raw_data_increase['Market Cap(USD)'].append(market_cap_rounded)
    #         raw_data_increase.setdefault('%24hr', [])
    #         raw_data_increase['%24hr'].append(percent_change_24)
    #         raw_data_increase.setdefault('Price(USD)', [])
    #         raw_data_increase['Price(USD)'].append(price_rounded)

    #     df = pd.DataFrame(raw_data_increase,
    #                         columns=['Name', 'Market Cap(USD)', '%24hr', 'Price(USD)'])

    #     print(df.to_string(index=False))

    #     # set fig size
    #     fig, ax = plt.subplots(figsize=(6.8, 2))
    #     # no axes
    #     ax.xaxis.set_visible(False)
    #     ax.yaxis.set_visible(False)
    #     # no frame
    #     ax.set_frame_on(False)
    #     # plot table
    #     tab = table(ax, df, rowLabels=[''] * df.shape[0], loc='center')
    #     # set font manually
    #     tab.auto_set_font_size(False)
    #     tab.set_fontsize(8.8)
    #     # set scale
    #     tab.scale(1, 1.8)
    #     # save the result
    #     plt.savefig('coincapinc.png')

    #     await ctx.send(file="coincapinc.png")


def setup(bot):
    bot.add_cog(Crypto(bot))

import requests
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


def setup(eolas):
    eolas.add_cog(Crypto(eolas))

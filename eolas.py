import discord
from discord.ext import commands

from config import config

import random
import sys, traceback

description = """There are a number of utility commands being showcased here."""
bot = commands.Bot(command_prefix="?", description=description)


cogs = ["cogs.members", "cogs.basic", "cogs.crypto", "cogs.news"]

# 'extensions.weather',
# 'extensions.football',
# 'extensions.games',
# 'extensions.news',
# 'extensions.crypto'


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ["?", "!"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return "?"

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description="A bot to have fun")


@bot.event
async def on_ready():

    print(f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(
        activity=discord.Streaming(name="True knowledge", url="https://www.google.com")
    )
    print(f"Successfully logged in and booted...!")


@bot.event
async def on_message(message):

    hello_list = ["Yo", "yo", "Hey", "hey", "Salut", "salut", "Bonjour", "bonjour"]
    foot_list = [
        "Neymar",
        "neymar",
        "PSG",
        "psg",
        "Zidane",
        "zidane",
        "Barca",
        "barca",
        "OM",
        "Deschamps",
        "deschamps",
        "Blaise",
        "blaise",
        "foot",
    ]
    meats = [
        "viande",
        "boeuf",
        "steak",
        "barbecue"
    ]
    meats_gifs = [
        "https://media.giphy.com/media/jxNyPO2icEEYSyZhoh/giphy.gif",
        "https://media.giphy.com/media/10ADU4ag31l63C/giphy.gif",
        "https://media.giphy.com/media/c11ISnPiRdis8/giphy.gif",
    ]

    if message.content in hello_list:
        await message.channel.send("Salut !")
    if any(i in message.content for i in foot_list):
        await message.channel.send("https://media.giphy.com/media/hBO3iUfEtI2s0/giphy.gif")
        await message.channel.send("Non, pas de ça ici, s'il-vous-plaît.")
    if any(i in message.content for i in meats):
        await message.channel.send(random.choice(meats_gifs))
    await bot.process_commands(message)


if __name__ == "__main__":
    for extension in cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()

bot.run(config.DISCORD_TOKEN, bot=True, reconnect=True)

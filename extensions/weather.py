import pyowm
import discord
from discord.ext import commands as eolas
from functools import partial

owm_key = ('YOU_OWM_API_KEY')

class Weather:
    def __init__(self, eolas):
        self.eolas = eolas

        # ?meteo <location> - Print the forecast of a specific location.
        @eolas.command()
        async def meteo(*, name):
            owm = pyowm.OWM(owm_key, language='fr')

            observation = owm.weather_at_place(name)
            weather = observation.get_weather()
            location = observation.get_location()
            get_temperature = weather.get_temperature(unit='celsius')
            get_wind = weather.get_wind()

            await eolas.say('Lieu: {}'.format(location.get_name()))
            await eolas.say('Température: {}'.format(
                get_temperature['temp']) + u'\N{DEGREE SIGN}C')
            await eolas.say(
                'Vitesse du vent: {}'.format(get_wind['speed']) + ' m/s')
            await eolas.say(
                'Description: {}'.format(weather.get_detailed_status()))


def setup(eolas):
    eolas.add_cog(Weather(eolas))

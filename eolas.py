from discord.ext import commands


description = '''There are a number of utility commands being showcased here.'''
eolas = commands.Bot(command_prefix='?', description=description)

token = 'YOUR_BOT_TOKEN'

extensions = (
    'extensions.basic',
    'extensions.weather',
    'extensions.football',
    'extensions.games',
    'extensions.news',
)


def main():
    @eolas.event
    async def on_ready():
        print('Logged in as')
        print(eolas.user.name)
        print(eolas.user.id)
        print('------')

    for extension in extensions:
        try:
            eolas.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    eolas.run(token)


if __name__ == '__main__':
    main()

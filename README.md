# Eòlas

### A Discord bot written in Python 3.6+
___
### Commands

|Command|Description|Usage|
|---|---|---|
|`add`|Adds two numbers together|`?add <123 1548>`|
|`roll`|Rolls a die in NdN format|`?roll <2d6>`|
| `choose` | For when you want to randomly choose something | `?choose <A B C>` |
| `repeat` | Repeats a message multiple times | `?repeat <5 oh>` |
| `joined` | Returns when a member joined the server. | `?joined <member>` |
| `cool` | Returns if a user is cool. In reality this just checks if a subcommand is being invoked. | `?cool <member>` |
| `news` | Scrape a specific block on lemonde.fr then return the news from it and append the data to a .CSV | `?news` |
| `facts` | Scrape unkno.com and return the fact from it. | `?facts` |
| `chess` | Print a link of a randomly selected puzzle from Lichess.org. | `?chess` |
| `meteo` | Print the forecast of a specific location. | `?meteo <location>` |
| `cavani` | Print a random gif of football player Edinson Cavani. | `?cavani` |
| `gwent` | Print the top 5 decks of the week on gwentdb.com | `?gwent` |
| `coins` | Print the top 5 coins on https://coinmarketcap.com/ | `?coins` |
| `coinschanges` | Print the top 5 increase (in %) in the last 24 hours. | `?coinschanges` |
| `space` | Fetch the latest news on spaceflightnow.com | `?space` |

 ### Events
 
 * on_message - Says "Salut !" when a member posts one of the hello messages from the list.
 * on_message - Responds with a gif and a message when it detects a certain keyword from the foot_list posted on a channel.

___

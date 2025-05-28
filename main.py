import discord

from discord.ext import commands
from os import listdir
from util import prefix, logging
from enum import Enum

COGS_PATH = 'cogs'

class CogStatus(Enum):
    WAITING = "WAITING"
    LOADED = "LOADED"


COGS = {}

for cog in listdir(COGS_PATH):
    if cog.endswith(".py"):
        name = cog[:-3]  # Remove the .py extension
        COGS[f"{COGS_PATH}.{name}"] = CogStatus.WAITING


async def loadCogs() -> None:
    for cog, status in COGS.items():
        if status == CogStatus.WAITING:
            print(f"loading {cog}")
            await bot.load_extension(cog)
            COGS[cog] = CogStatus.LOADED


## TODO storely secure TOKEN (maybe environment variable)
TOKEN = ''
DESCRIPTION = ''

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    command_prefix=prefix.getPrefix, description=DESCRIPTION, intents=INTENTS
)

@bot.event
async def on_ready():
    """
    This coroutine is called when the bot is connected to Discord.
        Note:
            `on_ready` doesn't take any arguments.

        Documentation:
            https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
    """
    print(f"{bot.user} has logged in.")
    await loadCogs()


bot.run(TOKEN, log_handler=logging.getDefaultLogHandler())

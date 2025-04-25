import discord
from discord.ext import commands
from os import listdir

from util import prefix, logging

## TODO storely secure TOKEN (maybe environment variable)

TOKEN = "MTM2NDM5Njg4Mzk3NTYwMjI2OQ.GrOl8l.bDMGX2UD-yOv70dGA6IEN4hJTqxtuVSmscO_0o"
DESCRIPTION = ""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=prefix.getPrefix, description=DESCRIPTION, intents=intents
)


async def loadCogs() -> None:
    """
    Loads the cogs from the `./cogs` folder.

    Notes:
        The cogs are .py files.
        The cogs are named in this format `{cog_dir}.{cog_filename_without_extension}`.
    """
    for cog in listdir("./cogs"):
        if cog.endswith(".py") == True:
            print(f"loading cogs.{cog[:-3]}")
            await bot.load_extension(f"cogs.{cog[:-3]}")


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

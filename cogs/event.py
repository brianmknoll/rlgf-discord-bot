import requests
import discord
from util.logging import logger

# import pdb; pdb.set_trace()

from datetime import datetime, timedelta
from discord.ext import commands
from config import BotConfig
from util.auth import SERVER_URL, getAuthHeaders


EVENTS_URI = f"{SERVER_URL}/events"


class EventCog(commands.Cog):
    """This is a cog with CRUD functions for events
    Note:
        All cogs inherits from `commands.Cog`_.
        All cogs are classes.
        All cogs needs a setup function (see below).

    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
    """

    def __init__(self, bot):
        self.bot = bot
        print("bot loaded")

    @commands.command(name="echo")
    async def echo(self, ctx, *, message):
        """This command outputs the string that is being passed as argument.
        Args:
                self
                ctx
                *, message (this sets the 'consume rest' behaviour for arguments)
        """
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logger.warning("Bot does not have permission to delete messages.")
        except discord.NotFound:
            logger.warning(
                "Original message not found, might have been already deleted."
            )

        await ctx.send(message)

    @commands.command(name="event")
    async def event(self, ctx, *, message):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return
        r = requests.post(
            EVENTS_URI,
            headers=await getAuthHeaders(),
            json={"guildId": f"{ctx.guild.name}__{ctx.guild.id}", "name": message},
        )
        print(r.raise_for_status())
        if r.status_code // 100 != 2:
            await ctx.send(f"Error creating event: {r.text}")
        else:
            await ctx.send(f'Event "{message}" created in server {ctx.guild.name}.')

    @commands.command(name="silence")
    async def silence(self, ctx, *, message=None):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logger.warning("Bot does not have permission to delete messages.")
        except discord.NotFound:
            logger.warning(
                "Original message not found, might have been already deleted."
            )

        if not message:
            BotConfig.silence()
            await ctx.send("The bot has been silenced")
        else:
            minutes = 0
            try:
                minutes = int(message)
            except:
                await ctx.send(f'Failed to convert "{message}" into minutes')
                return
            delta = timedelta(minutes=minutes)
            BotConfig.set_silence(datetime.now() + delta)
            await ctx.send(f"The bot has been silenced for {minutes} mins")

    @commands.command(name="wake")
    async def wake(self, ctx):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logger.warning("Bot does not have permission to delete messages.")
        except discord.NotFound:
            logger.warning(
                "Original message not found, might have been already deleted."
            )

        BotConfig.remove_silence()
        await ctx.send("The bot is awake")


async def setup(bot):
    """Every cog needs a setup function like this."""
    await bot.add_cog(EventCog(bot))

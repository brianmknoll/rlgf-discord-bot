import requests

from discord.ext import commands


SERVER_URL='https://rlgf-service-821668527340.us-west1.run.app'
EVENTS_URI=f'{SERVER_URL}/events'


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
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="event")
    async def event(self, ctx, *, message):
        if ctx.guild is None:
            await ctx.send('This command can only be used in a server.')
            return
        r = requests.post(EVENTS_URI, json={
            'guild_id': f'{ctx.guild.name}__{ctx.guild.id}',
            'name': message
        })
        print(r.raise_for_status())
        if r.status_code // 100 != 2:
            await ctx.send(f'Error creating event: {r.text}')
        else:
            await ctx.send(f'Event "{message}" created in server {ctx.guild.name}.')


async def setup(bot):
    """Every cog needs a setup function like this."""
    await bot.add_cog(EventCog(bot))

from discord.ext import commands
import discord


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


async def setup(bot):
    """Every cog needs a setup function like this."""
    await bot.add_cog(EventCog(bot))

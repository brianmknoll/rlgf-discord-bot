from discord.ext import commands


class UptimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        await ctx.message.delete()
        await ctx.send(get_uptime())


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    raise Exception("Could not read uptime from /proc/uptime")


async def setup(bot):
    await bot.add_cog(UptimeCog(bot))

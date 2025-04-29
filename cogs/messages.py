from discord.ext import commands

class MessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def greet_new_member(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the server, {member.mention}!")

async def setup(bot):
    await bot.add_cog(MessagesCog(bot))
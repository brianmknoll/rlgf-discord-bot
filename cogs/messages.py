import json
import requests

from discord.ext import commands
from random import random
from ai.router_ai import route_generate
from ai.sassy_ai import sassy_ai_generate
from config import BotConfig
from models.memory import get_memories
from models.messages import upsert_message_and_get_thread
from util.logging import logger


class MessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def greet_new_member(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the server, {member.mention}!")

    @commands.Cog.listener("on_message")
    async def handle_new_message(self, message):
        logger.debug('handling new message')
        memories = await get_memories(message)
        contents = await upsert_message_and_get_thread(message)
        if message.author != self.bot.user:
            action = route_generate(contents, memories)
            if not action:
                return
            
            logger.debug(json.dumps(action))

            # TODO: Clean up this if-else branching. It looks messy to me.
            
            if (action['intent'] == 'quiet'):
                logger.debug(f'Quieting: {action["reason"]}')
                # Fall through and maybe generate a sassy response...
            elif (action['intent'] == 'remember'): 
                logger.debug(f'Remembering: {action["memory"]}')
                return
            elif (action['intent'] == 'schedule'):
                logger.debug(f'Scheduling: {action["schedule"]}')
                return
            elif (action['intent'] == 'respond'):
                if BotConfig.is_silent():
                    logger.info('Will not respond. The bot has currently been silenced.')
                    return
                logger.debug(f'Responding: {action["response"]}')
                await message.channel.send(action['response'])
                return
            r = random()
            logger.debug(f'r is {r}; running? {r > 0.96}')
            if r > 0.96:
                if BotConfig.is_silent():
                    logger.info('Will not make sarcastic comment. The bot has currently been silenced.')
                else:
                    await message.channel.send(sassy_ai_generate(contents))


async def setup(bot):
    await bot.add_cog(MessagesCog(bot))


from typing import List
import discord
from discord.ext import commands


def getPrefix(bot: commands.Bot, message: discord.Message) -> str | List[str]:
    """
    This function returns a Prefix for our bot's commands.

    Args:
            bot (commands.Bot): The bot that is invoking this function.
            message (discord.Message): The message that is invoking.

    Returns:
            string or iterable containing strings: A string containing prefix or an iterable containing prefixes
    """
    if not isinstance(message.guild, discord.Guild):
        """Checks if the bot isn't inside of a guild.
        Returns a prefix string if true, otherwise passes.
        """
        return "!"

    return ["!", "?", ">", "/"]

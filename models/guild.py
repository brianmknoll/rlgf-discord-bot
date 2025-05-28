from util.auth import SERVER_URL


GUILDS_URI=f'{SERVER_URL}/guilds'


def get_guild_id(message):
  return f'{message.guild.name}__{message.guild.id}'


def get_guild(message):
  pass
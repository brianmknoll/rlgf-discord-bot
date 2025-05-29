import requests
from api.client import get, post
from models.guild import get_guild_id
from util.auth import SERVER_URL, getAuthHeaders


MEMORY_URI=f'{SERVER_URL}/memory'


async def upload_memory(message, memory):
  await post(
      MEMORY_URI,
      headers=await getAuthHeaders(),
      json={
          'guildId': get_guild_id(message),
          'memory': memory,
      }
  )


async def get_memories(message):
  payload = await get(
    MEMORY_URI,
    params={
        'guild_id': get_guild_id(message),
    }
  )
  return payload.get('memory', [])
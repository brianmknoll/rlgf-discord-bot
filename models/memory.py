import requests
from models.guild import get_guild_id
from util.auth import SERVER_URL, getAuthHeaders


MEMORY_URI=f'{SERVER_URL}/memory'


def upload_memory(message, memory):
  r = requests.post(
      MEMORY_URI,
      headers=getAuthHeaders(),
      json={
          'guildId': get_guild_id(message),
          'memory': memory,
      }
  )
  print(r.raise_for_status())
  if r.status_code // 100 != 2:
      raise Exception(f'Error creating memory: {r.text}')


def get_memories(message):
  r = requests.get(
    MEMORY_URI,
    headers=getAuthHeaders(),
    params={
        'guild_id': get_guild_id(message),
    }
  )
  print(r.raise_for_status())
  if r.status_code // 100 != 2:
      raise Exception(f'Error getting memories: {r.text}')
  payload = r.json()
  return payload.get('memory', [])
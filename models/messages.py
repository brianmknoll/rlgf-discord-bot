import requests

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
from models.channel import get_channel_id
from models.guild import get_guild_id
from util.logging import logger
from util.auth import SERVER_URL, getAuthHeaders


MESSAGES_URI=f'{SERVER_URL}/message'
CONTACT_BOT_AUTHOR = 'Contact Bot'


@dataclass
class ThreadMessage:
  author: str
  message: str
  timestamp: datetime
  is_bot = False

  @staticmethod
  def from_bot(message: str, timestamp: datetime):
      msg = ThreadMessage(
          author=CONTACT_BOT_AUTHOR,
          message=message,
          timestamp=timestamp,
      )
      msg.is_bot = True
      return msg



async def upsert_message_and_get_thread(message):
  epoch = int(message.created_at.timestamp() * 1000)
  r = requests.post(
      MESSAGES_URI, 
      headers=await getAuthHeaders(),
      json={
          'author': message.author.name,
          'guildId': get_guild_id(message),
          'channel': get_channel_id(message),
          'message': message.content,
          'timestamp': epoch,
      }
  )
  throw_if_bad_status(r, ignore_conflict=True)
  
  r = requests.get(
    MESSAGES_URI,
    headers=await getAuthHeaders(),
    params={
      'channel_id': get_channel_id(message),
      'guild_id': get_guild_id(message),
    }
  )
  throw_if_bad_status(r)

  msgs = r.json()

  content: List[ThreadMessage] = []
  for m in msgs:
    author = m['author']
    message = m['message']
    timestamp = datetime.strptime(
      m['timestamp'], 
      "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)
    if m['author'] == CONTACT_BOT_AUTHOR:
        content.append(ThreadMessage.from_bot(message, timestamp))
    else:
        content.append(ThreadMessage(author, message, timestamp))
  return content


def throw_if_bad_status(r, *, ignore_conflict=False):
  try:
    print(r.raise_for_status())
  except requests.exceptions.HTTPError:
    if r.status_code == 409 and ignore_conflict:
      logger.debug("AlreadyExists; continuing without error.")
    else:
      raise
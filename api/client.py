import requests

from util.auth import getAuthHeaders
from util.logging import logger


async def post(url, body, *, ignore_conflict=False):
  r = requests.post(
    url,
    headers=await getAuthHeaders(),
    json=body
  )
  throw_if_bad_status(r, ignore_conflict=ignore_conflict)
  if r.text and r.headers.get("content-type") == 'application/json':
    return r.json()
  else:
    return None


async def get(url, *, query_params=None):
  r = requests.get(
    url,
    headers=await getAuthHeaders(),
    params=query_params
  )
  throw_if_bad_status(r)
  if r.text and r.headers.get("content-type") == 'application/json':
    return r.json()
  else:
    return None
  

def throw_if_bad_status(r, *, ignore_conflict=False):
  try:
    print(r.raise_for_status())
  except requests.exceptions.HTTPError:
    if r.status_code == 409 and ignore_conflict:
      logger.debug("AlreadyExists; continuing without error.")
    else:
      raise
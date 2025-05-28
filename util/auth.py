import asyncio
import google.oauth2.id_token
import google.auth.transport.requests
import time
import json

from util.logging import logger
from functools import partial
from jwt.utils import base64url_decode


SERVER_URL = 'https://rlgf-service-821668527340.us-west1.run.app'
_CACHED_ID_TOKEN = None
_TOKEN_EXPIRY_TIME = 0
_TOKEN_FETCH_LOCK = asyncio.Lock() # To prevent multiple concurrent fetches


def decode_jwt_payload(token):
    try:
        _, payload_segment, _ = token.split('.', 2)
        payload_segment += '=' * (-len(payload_segment) % 4)
        decoded_payload = base64url_decode(payload_segment)
        return json.loads(decoded_payload.decode('utf-8'))
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None


async def getGcpIdToken():
    global _CACHED_ID_TOKEN, _TOKEN_EXPIRY_TIME

    if _CACHED_ID_TOKEN and _TOKEN_EXPIRY_TIME > (time.time() + 60):
        return _CACHED_ID_TOKEN

    async with _TOKEN_FETCH_LOCK:
        if _CACHED_ID_TOKEN and _TOKEN_EXPIRY_TIME > (time.time() + 60):
            return _CACHED_ID_TOKEN

        logger.info("Fetching new GCP ID token...")
        loop = asyncio.get_event_loop()
        request = google.auth.transport.requests.Request()
        blocking_task = partial(google.oauth2.id_token.fetch_id_token, request, SERVER_URL)
        
        try:
            new_token = await loop.run_in_executor(None, blocking_task)
            if new_token:
                _CACHED_ID_TOKEN = new_token
                payload = decode_jwt_payload(new_token)
                if payload and 'exp' in payload:
                    _TOKEN_EXPIRY_TIME = payload['exp']
                else:
                    # Default to a shorter expiry if 'exp' not found, or handle error
                    _TOKEN_EXPIRY_TIME = time.time() + 3500 # Approx 1 hour default
                logger.info(f"Successfully fetched and cached new token. Expires at: {_TOKEN_EXPIRY_TIME}")
            return new_token
        except Exception as e:
            logger.error(f"Error fetching GCP ID token: {e}")
            _CACHED_ID_TOKEN = None
            _TOKEN_EXPIRY_TIME = 0
            return None


async def getAuthHeaders():
    id_token = await getGcpIdToken()
    if id_token:
        return {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
        }
    return {}
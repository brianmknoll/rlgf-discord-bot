import google.auth.transport.requests
import google.oauth2.id_token

from util.logging import logger


SERVER_URL = 'https://rlgf-service-821668527340.us-west1.run.app'
ID_TOKEN = None


def getGcpIdToken():
    """Get the ID token from the Google Cloud Run service.

    Returns:
        str: The ID token.
    """
    global ID_TOKEN
    if ID_TOKEN is None:
        logger.info(f'Fetching ID token for audience: {SERVER_URL}')
        try:
            request = google.auth.transport.requests.Request()
            ID_TOKEN = google.oauth2.id_token.fetch_id_token(request, SERVER_URL)
        except Exception as e:
            logger.error(f"Error fetching ID token using google-auth: {e}")
    return ID_TOKEN


def getAuthHeaders():
    """Get the authorization headers for the Google Cloud Run service.

    Returns:
        dict: The authorization headers.
    """
    id_token = getGcpIdToken()
    return {
        'Authorization': f'Bearer {id_token}',
        'Content-Type': 'application/json'
    }
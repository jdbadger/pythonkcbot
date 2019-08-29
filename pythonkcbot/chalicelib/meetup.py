import logging

from chalicelib.models import Event

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_request(url):
    """
    Http request handler.
    """

    try:

        r = requests.get(url)
        r.raise_for_status()
        return r.json()
   
    except requests.exceptions.RequestException as e:

        logger.error(f"A request exception occurred: {e}")
        raise e
    

def get_events():
    """
    Http response handler for request to Meetup API.
    """

    url = "http://api.meetup.com/pythonkc/events"

    try:

        events = make_request(url)
        return (Event(name=e["name"], date=e["local_date"], link=e["link"], status=e["status"]) for e in events)
    
    except Exception as e:
        
        logger.error(f"An error occured while handling the response: {e}")
        raise e
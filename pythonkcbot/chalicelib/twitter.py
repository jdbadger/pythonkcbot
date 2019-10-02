import logging
import os

import tweepy


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_api():
    """
    Create an instance of tweepy.API based on provided credentials
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:

        api.verify_credentials()

    except Exception as e:

        logger.error(f"An error occurred while verifying credentials: {e}")
        raise e
        
    return api

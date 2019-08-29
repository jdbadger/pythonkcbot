import os
from unittest.mock import Mock, patch

from chalicelib.twitter import create_api

import tweepy
import pytest


@patch('chalicelib.twitter.os.getenv')
@patch('chalicelib.twitter.tweepy.OAuthHandler')
@patch('chalicelib.twitter.tweepy.API')
def test_create_api(mock_api, mock_oauthhandler, mock_getenv):
    with patch('chalicelib.twitter.logger') as mock_logger:
        api = create_api()
        mock_getenv.assert_called()
        mock_oauthhandler.assert_called_with(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
        mock_oauthhandler.return_value.set_access_token.assert_called_with(os.getenv("ACCESS_TOKE"), os.getenv("ACCESS_TOKEN_SECRET"))
        mock_api.assert_called_with(mock_oauthhandler.return_value, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        mock_logger.error.assert_not_called()
        mock_api.return_value.verify_credentials.assert_called()


@patch('chalicelib.twitter.os.getenv')
@patch('chalicelib.twitter.tweepy.OAuthHandler')
@patch('chalicelib.twitter.tweepy.API')
def test_create_api_raises_exception(mock_api, mock_oauthhandler, mock_getenv):
    with patch('chalicelib.twitter.logger') as mock_logger:
        with pytest.raises(Exception):
            mock_api.return_value.verify_credentials.side_effect = tweepy.error.TweepError('')
            api = create_api()
            mock_getenv.assert_called()
            mock_oauthhandler.assert_called_with(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
            mock_oauthhandler.return_value.set_access_token.assert_called_with(os.getenv("ACCESS_TOKE"), os.getenv("ACCESS_TOKEN_SECRET"))
            mock_api.assert_called_with(mock_oauthhandler.return_value, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            mock_api.return_value.verify_credentials.assert_called()
        mock_logger.error.assert_called_with("An error occurred while verifying credentials: ")
import json
from unittest.mock import Mock, patch

from chalicelib.meetup import make_request, get_events

import pytest
import requests


def _mock_response(status_code=200, json=None, raise_for_status=None):
    """
    Helper function to generate mock response objects.
    """
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    if json:
        mock_resp.json = Mock(return_value=json)
    return mock_resp


@patch("chalicelib.meetup.requests.get")
def test_make_request(mock_get):
    url = "http://api.meetup.com/pythonkc/events"
    json_data = '{"name": "PythonKC Coffee & Code", "local_date": "2020-02-02", "link": "http://api.meetup.com/pythonkc/events/1", "status": "upcoming"}'
    mock_response = _mock_response(status_code=200, json=json_data)
    mock_get.return_value = mock_response
    response = make_request(url)
    mock_get.assert_called_with(url)
    mock_response.raise_for_status.assert_called()
    mock_response.json.assert_called()
    assert response == json_data


@patch("chalicelib.meetup.requests.get")
def test_make_request_raises_exception(mock_get):
    mock_response = _mock_response(
        status_code=500,
        json={"error": "not found"},
        raise_for_status=requests.exceptions.RequestException,
    )
    mock_get.return_value = mock_response
    with patch("chalicelib.meetup.logger") as mock_logger:
        with pytest.raises(requests.exceptions.RequestException):
            url = "http://api.meetup.com/pythonkc/events"
            response = make_request(url)
            mock_get.assert_called_with(url)
            mock_response.raise_for_status.assert_called()
            mock_get.json.assert_not_called()
            assert response == None
        mock_logger.error.assert_called_with("A request exception occurred: ")


@patch("chalicelib.meetup.make_request")
def test_get_events(mock_make_request):
    json_data = '{"name": "PythonKC Coffee & Code", "local_date": "2020-02-02", "link": "http://api.meetup.com/pythonkc/events/1", "status": "upcoming"}'
    mock_make_request.return_value = [json.loads(json_data)]
    with patch("chalicelib.meetup.logger") as mock_logger:
        events = get_events()
        mock_make_request.assert_called_with("http://api.meetup.com/pythonkc/events")
        mock_logger.error.assert_not_called()
        assert events is not None


@patch("chalicelib.meetup.make_request")
def test_get_events_raises_exception(mock_make_request):
    mock_make_request.side_effect = Exception
    with patch("chalicelib.meetup.logger") as mock_logger:
        with pytest.raises(Exception):
            events = get_events()
            mock_make_request.assert_called_with(
                "http://api.meetup.com/pythonkc/events"
            )
            assert events is None
        mock_logger.error.assert_called_with(
            "An error occured while handling the response: "
        )

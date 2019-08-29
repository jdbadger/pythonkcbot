import datetime
from unittest.mock import Mock, patch

patch("app.Chalice").start()

from chalicelib.models import Event
from app import announce

import pytest


def _today_plus(days):
    return datetime.date.isoformat(
        datetime.date.today() + datetime.timedelta(days=days)
    )


@patch("chalicelib.meetup.Event.tweet")
@patch("app.create_api")
@patch("app.get_events")
def test_announce(mock_get_events, mock_create_api, mock_tweet):
    test_event = {
        "account": "1234567890",
        "detail": {},
        "detail-type": "Scheduled Event",
        "id": "12345678-bpf1-4667-9c5e-39f98e9a6113",
        "region": "us-west-2",
        "resources": [
            "arn:aws:events:us-west-2:1234567890:rule/testevents-dev-every-day"
        ],
        "source": "aws.events",
        "time": "2019-07-30T23:28:38Z",
        "version": "0",
    }
    test_context = None
    meetup_events = [
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(10),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "upcoming",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(2),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "upcoming",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(1),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "upcoming",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(10),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "cancelled",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(2),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "cancelled",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(1),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "cancelled",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(9),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "upcoming",
        },
        {
            "name": "PythonKC Coffee & Code",
            "local_date": _today_plus(6),
            "link": "https://www.meetup.com/pythonkc/events/test_event",
            "status": "cancelled",
        },
    ]
    mock_get_events.return_value = (
        Event(name=e["name"], date=e["local_date"], link=e["link"], status=e["status"])
        for e in meetup_events
    )
    announce(test_event, test_context)
    mock_get_events.assert_called()
    mock_create_api.assert_called()
    mock_create_api.return_value.update_status.assert_called()
    mock_tweet.assert_called()
    assert mock_tweet.call_count == 3

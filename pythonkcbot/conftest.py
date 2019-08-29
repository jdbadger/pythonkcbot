import datetime

from chalicelib.models import Event

import pytest

# helper
def _today_plus(days):
    return datetime.date.isoformat(datetime.date.today() + datetime.timedelta(days=days))

# FIXTURES

@pytest.fixture
def make_event():

    def _make_event(days=10, status="upcoming"):

        return Event(name="test event", date=_today_plus(days), link="www.api.meetup.com/pythonkc/event/1", status=status)

    return _make_event
import datetime

from chalicelib.models import Event

import pytest


def test_event_hasattr_name(make_event):
    event = make_event()
    assert hasattr(event, "name")


def test_event_name_type_str(make_event):
    event = make_event()
    assert f"{type(event.name)}" == "<class 'str'>"


def test_event_hasattr_date(make_event):
    event = make_event()
    assert hasattr(event, "date")


def test_event_date_type_str(make_event):
    event = make_event()
    assert f"{type(event.date)}" == "<class 'str'>"


def test_event_hasattr_link(make_event):
    event = make_event()
    assert hasattr(event, "link")


def test_event_link_type_str(make_event):
    event = make_event()
    assert f"{type(event.link)}" == "<class 'str'>"


def test_event_hasattr_status(make_event):
    event = make_event()
    assert hasattr(event, "status")


def test_event_status_type_str(make_event):
    event = make_event()
    assert f"{type(event.status)}" == "<class 'str'>"


def test_method_str(make_event):
    event = make_event()
    expected = f"{event.date} - {event.name}"
    assert str(event) == expected


def test_property_date_natural(make_event):
    event = make_event()
    expected = datetime.date.fromisoformat(f"{event.date}").strftime("%A, %B %d")
    assert event.date_natural == expected


def test_property_days_until(make_event):
    event = make_event()
    d = datetime.date.fromisoformat(f"{event.date}") - datetime.date.today()
    expected = d.days
    assert event.days_until() == expected


@pytest.mark.parametrize('test_input, expected', [([1, "upcoming"], True), ([2, "upcoming"], True), ([10, "upcoming"], True), ([3, "upcoming"], False), ([1, "cancelled"], False)])
def test_method_is_target_event(test_input, expected, make_event):
    event = make_event(test_input[0], test_input[1])
    assert event.is_target_event() == expected


def test_method_tweet_days_until_10(make_event):
    event = make_event(days=10)
    assert event.tweet() == f"RSVPs are open! Join us for our upcoming {event.name} on {event.date_natural}! Event details here: {event.link}"


def test_method_tweet_days_until_2(make_event):
    event = make_event(days=2)
    assert event.tweet() == f"Join us for our upcoming {event.name} on {event.date_natural}! Event details and RSVP here: {event.link}"


def test_method_tweet_days_until_1(make_event):
    event = make_event(days=1)
    assert event.tweet() == f"KC Pythonistas - Join us tomorrow for {event.name}! Event details and RSVP here: {event.link}"


def test_method_tweet_days_until_3(make_event):
    event = make_event(days=3)
    assert event.tweet() == None

from chalice import Chalice
from chalice.app import Cron
from chalicelib.meetup import get_events
from chalicelib.twitter import create_api


app = Chalice(app_name="pythonkcbot")

# invoked daily at 5pm UTC / 12pm Central
@app.schedule(Cron(0, 17, "*", "*", "?", "*"))
def announce(event):

    # get events from the Meetup API events group/events endpoint.
    events = get_events()

    if events:

        # create an instance of tweepy.API to interact with the twitter api
        api = create_api()

        for e in events:

            # If target event, send corresponding tweet.
            if e.is_target_event():

                api.update_status(e.tweet())

            else:

                continue

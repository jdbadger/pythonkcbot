from dataclasses import dataclass
import datetime


@dataclass
class Event:

    name: str
    date: str
    link: str
    status: str

    def __str__(self):

        return f"{self.date} - {self.name}"

    @property
    def date_natural(self):

        return datetime.date.fromisoformat(f"{self.date}").strftime("%A, %B %d")

    def days_until(self):
        """
        Returns number of days represented in timedetla object
        resulting from event date object minus current date object.
        """

        d = datetime.date.fromisoformat(f"{self.date}") - datetime.date.today()
        return d.days

    def is_target_event(self):
        """
        Returns True if conditions are met that qualify event
        as target event; False if not.
        """

        if self.days_until() in (1, 2, 10) and self.status == "upcoming":

            return True

        return False

    def tweet(self):
        """
        Returns unique tweet string given Event object attributes.
        """

        tweet_dict = {
            "1" : f"Hey, KC Pythonistas! Join us tomorrow for {self.name}! Event details and RSVP here: {self.link}",
            "2" : f"Join us for our upcoming {self.name} on {self.date_natural}! Event details and RSVP here: {self.link}",
            "10" : f"RSVPs are open! Join us for our upcoming {self.name} on {self.date_natural}! Event details here: {self.link}"
        }

        tweet_key = str(self.days_until())

        return tweet_dict.get(tweet_key)
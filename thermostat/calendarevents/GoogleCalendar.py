from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleCalendar:
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

    def __init__(self, credential_name):
        """
        Establishes credentials/token needed to connect to Google Calendar API
        :param credential_name: Name of the file containing credentials from Google API
        """
        self.credential_name = credential_name
        self.store = file.Storage("thermostat/calendarevents/token.json")
        self.credentials = self.store.get()
        self.service = build('calendar', 'v3', http=self.credentials.authorize(Http()))

        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(self.credentialName, self.SCOPES)
            self.credentials = tools.run_flow(flow, self.store)
        self.events = []

    def get_events(self, num_events):
        """
        Fetches events from Google Calendar
        :param num_events: Number of events to fetch
        :return: list of events fetched from Google Calendar
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=num_events, singleEvents=True,
                                                   orderBy='startTime').execute()
        self.events = events_result.get('items', [])

        if not self.events:
            print("there are no upcoming events in the calendar")

        return self.events

    def write_events_to_file(self, num_events):
        """
        Write the upcoming events from the calendar to a text file
        :param num_events: Number of events to fetch from Google Calendar to write to the text file
        :return: None
        """
        if num_events < 0:
            return False

        self.events = self.get_events(num_events)
        f = open("thermostat/calendarevents/events.txt", "w")
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            f.write(start + " " + event['summary'])
        f.close()

from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class CalendarEvents:
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

    def __init__(self, credential_name):
        self.credential_name = credential_name
        self.store = file.Storage("CalendarEvents/token.json")
        self.credentials = self.store.get()
        self.service = build('calendar', 'v3', http=self.credentials.authorize(Http()))

        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(self.credentialName, self.SCOPES)
            self.credentials = tools.run_flow(flow, self.store)

    def get_events(self, num_events):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=num_events, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("there are no upcoming events in the calendar")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])

        return events

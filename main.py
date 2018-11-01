from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def setup_api():
    store = file.Storage("token.json")
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)

    global service
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

def get_events(numEvents):
    global upcoming_events
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=numEvents, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("there are no upcoming events in the calendar")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == "__main__":
    setup_api()
    get_events(10)
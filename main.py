import CalendarEvents

google_cal = CalendarEvents.CalendarEvents('credentials.json')

if __name__ == "__main__":
    events = google_cal.get_events(10)

    for event in events:
        print(event['summary'])
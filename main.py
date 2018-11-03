import CalendarEvents
from apscheduler.schedulers.background import BackgroundScheduler
import GUI

google_cal = CalendarEvents.CalendarEvents('credentials.json')
calendar_events = []

def refresh_calendar_events():
    fetched_events = google_cal.get_events(10)
    for event in fetched_events:
        print(event['summary'])
    check_for_new_events(fetched_events)

def check_for_new_events(fetched_events):
    global calendar_events
    new_event = False

    for fetched_event in fetched_events:
       for existing_event in calendar_events:
           if fetched_event is not existing_event:
               new_event = True
               calendar_events = fetched_events
               return new_event
    return new_event


if __name__ == "__main__":
    refresh_events_scheduler = BackgroundScheduler()
    refresh_events_scheduler.add_job(refresh_calendar_events, 'interval', seconds=10)

    try:
        refresh_events_scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        refresh_events_scheduler.shutdown()

    GUI.initialize()

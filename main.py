from CalendarEvents import CalendarEvents
from UI import GUI  # TODO consider making a python module to hold all files to be imported
from apscheduler.schedulers.background import BackgroundScheduler

google_cal = CalendarEvents.CalendarEvents('CalendarEvents/credentials.json')
calendar_events = google_cal.get_events(10)


def refresh_calendar_events():
    fetched_events = google_cal.get_events(10)
    for event in fetched_events:
        print(event['summary'])
    if check_for_new_events(fetched_events):
        print("we need to do some work")
    else:
        print("were chillin")


def check_for_new_events(fetched_events):
    global calendar_events

    for fetched_event in fetched_events:
        for existing_event in calendar_events:
            if fetched_event is not existing_event:
                calendar_events = fetched_events
                print("There is a new event")
                return True
    return False


def update_temperature():
    GUI.update_temperature()


if __name__ == "__main__":
    refresh_events_scheduler = BackgroundScheduler()
    refresh_events_scheduler.add_job(refresh_calendar_events, 'interval', seconds=10)

    update_current_temp_scheduler = BackgroundScheduler()
    update_current_temp_scheduler.add_job(update_temperature, 'interval', seconds=1)

    try:
        refresh_events_scheduler.start()
        update_current_temp_scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        refresh_events_scheduler.shutdown()
        update_current_temp_scheduler.shutdown()

    GUI.initialize()

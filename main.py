from thermostat.calendarevents import CalendarEvents
from thermostat.ui import GUI
from apscheduler.schedulers.background import BackgroundScheduler

google_cal = CalendarEvents.CalendarEvents('credentials.json')
calendar_events = google_cal.get_events(10)


def refresh_calendar_events():
    global calendar_events
    calendar_events = google_cal.get_events(10)


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

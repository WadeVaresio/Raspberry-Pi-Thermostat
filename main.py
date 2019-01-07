#!/usr/bin/env python3

from thermostat.calendarevents import GoogleCalendar
from thermostat.ui import GUI
from apscheduler.schedulers.background import BackgroundScheduler
from thermostat.database import Database

google_cal = GoogleCalendar('credentials.json')
MAX_AMOUNT_OF_EVENTS = 10


def refresh_calendar_events():
    """
    Refresh the calendar events and write any new events in the database
    :return: None
    """
    Database.add_to_queue(google_cal.get_events(MAX_AMOUNT_OF_EVENTS))
    Database.write_from_queue()


def update_temperature():
    GUI.update_temperature()


if __name__ == "__main__":
    refresh_events_scheduler = BackgroundScheduler()
    refresh_events_scheduler.add_job(refresh_calendar_events, 'interval', seconds=10)

    update_current_temp_scheduler = BackgroundScheduler()
    update_current_temp_scheduler.add_job(update_temperature, 'interval', minutes=5)

    try:
        refresh_events_scheduler.start()
        update_current_temp_scheduler.start()
        update_temperature()
        GUI.initialize()
    except (KeyboardInterrupt, SystemExit):
        refresh_events_scheduler.shutdown()
        update_current_temp_scheduler.shutdown()

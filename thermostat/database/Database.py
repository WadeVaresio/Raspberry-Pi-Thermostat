import sqlite3
import sys
if sys.version_info[0] != 3:
    sys.exit("This script requires Python 3")
from queue import Queue

QUEUE = Queue()
DATABASE_FILE = 'database'


def write_event(ID, start, end, temperature, creator):
    """
    Write an event to the database, checks if it exists already
    :param ID: ID of the event
    :param start: start time of the event
    :param end: end time of the event
    :param temperature: corresponding temperature
    :param creator: creator of the event (Name from the google account)
    :return: None
    """
    database = connect_to_database()

    if check_for_existing_event(ID):
        update_event(ID, start, end, temperature, creator)
        return

    database.execute("INSERT INTO EVENTS(ID, StartTime, EndTime, Temperature, Creator) VALUES (?, ? ,?, ?, ?)", [
        ID, start, end, temperature, creator])
    database.commit()


def remove_event_by_id(ID):
    """
    Remove an event based on it's ID
    :param ID: ID of the event to be removed
    :return: None
    """
    database = connect_to_database()
    database.execute("DELETE from EVENTS where ID = ?;", [ID])
    database.commit()


def print_all_events():
    """
    Prints all of the database events used for debugging purposes
    :return: None
    """
    database = connect_to_database()
    cursor = database.execute("SELECT ID, StartTime, EndTime, Temperature, Creator from EVENTS")

    for row in cursor:
        print("ID: " + str(row[0]))
        print("Start Time: " + row[1])
        print("End Time: " + row[2])
        print("Temperature: " + str(row[3]))
        print("Creator: " + row[4])


def add_to_queue(data):
    global QUEUE
    QUEUE.put(data)


def write_from_queue():
    """
    Write all of the events from the queue to the database. Will not add an event if it is scheduled for all day.
    :return:
    """
    for index in range(QUEUE.qsize()):
        events = QUEUE.get()
        check_for_deletions(events)
        for event in events:
            ID = event['id']
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')

            if not isinstance(start, str) or not isinstance(end, str):
                print("Event not added since it is an all day event")
                continue

            try:
                temp = float(event['summary'])
            except ValueError:
                print("ERROR, summary of event was not a number did not add to database")
                continue

            creator = event['creator'].get('displayName')

            write_event(ID, start, end, temp, creator)


def get_all_events():
    """
    Get all of the events stored in the database
    :return: All data from the EVENTS table in the database
    """
    database = connect_to_database()
    data = database.execute("SELECT ID, StartTime, EndTime, Temperature, Creator FROM EVENTS")
    return data


def check_for_existing_event(event_id):
    """
    Checks if existing event with the same ID exists
    :param event_id: ID of the event to check the database against
    :return: True if there is an existing event in the database with the same ID
    """
    database = connect_to_database()
    data = database.execute("SELECT ID from EVENTS")

    for row in data:
        if event_id == str(row[0]):
            return True
    return False


def check_for_deletions(data):
    """
    Check the new data from the queue against the current data stored for any deletions
    :param data: The new data from the queue
    :return: None
    """
    database = connect_to_database()

    database_data = []
    for old_event in database.execute("SELECT ID FROM EVENTS"):
        database_data.append(old_event[0])

    new_data = []
    for new_event in data:
        new_data.append(new_event['id'])

    for diff in set(database_data) - set(new_data):
        remove_event_by_id(diff)


def update_event(ID, start, end, temperature, creator):
    """
    Update an event in the database based off its ID
    :param ID: ID of the event you want to change
    :param start: start time to update the database entry
    :param end: end time to update the database entry
    :param temperature: temperature to update the database entry
    :param creator: creator to update the database entry
    :return: None
    """
    database = connect_to_database()
    database.execute("UPDATE EVENTS SET StartTime = ? WHERE ID = ?", [start, ID])
    database.execute("UPDATE EVENTS SET EndTime = ? WHERE ID = ?", [end, ID])
    database.execute("UPDATE EVENTS SET Temperature = ? WHERE ID = ?", [temperature, ID])
    database.execute("UPDATE EVENTS SET Creator = ? WHERE ID = ?", [creator, ID])
    database.commit()


def connect_to_database():
    """
    Connect to the SQLite database
    :return: SQLite3 Connection Object
    """
    return sqlite3.connect(DATABASE_FILE)


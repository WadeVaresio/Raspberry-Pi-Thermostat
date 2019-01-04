import sqlite3


class Database:

    def __init__(self, file_path):
        """
        Constructs a new database object responsible for communicating with the SQLite database
        :param file_path: File path to the database file
        :return: New Database object
        """
        if not isinstance(file_path, str):
            raise Exception("The filepath specified is invalid")

        self.database = sqlite3.connect(file_path)

    def write_event(self, id, date, temperature, creator):
        """
        Write an event to the database.
        :param id: ID for the data entry
        :param date: Date of the event
        :param temperature: Temperature corresponding to the calendar event
        :param creator: Creator of the event
        :return:
        """
        self.database.execute("INSERT INTO EVENTS(ID, Date, Temperature, Creator) VALUES (?, ? ,?, ?)", [
                id, date, temperature, creator])
        self.database.commit()

    def remove_event_by_id(self, id):
        """
        Remove an event based on it's ID
        :param id: ID of the event to be removed
        :return: None
        """
        self.database.execute("DELETE from EVENTS where ID = ?;", [id])
        self.database.commit()


    def print_all_events(self):
        """
        Prints all of the database events used for debugging purposes
        :return: None
        """
        cursor = self.database.execute("SELECT ID, Date, Temperature, Creator from EVENTS")

        for row in cursor:
            print("ID: " + str(row[0]))
            print("Date: " + row[1])
            print("Temperature: " + str(row[2]))
            print("Creator: " + row[3])

    def close_database(self):
        """
        Close the connection to the database
        :return: None
        """
        self.database.close()

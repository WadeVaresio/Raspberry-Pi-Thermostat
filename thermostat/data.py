CALENDAR_EVENTS = []
TEMPERATURE = float


def set_calendar_events(data):
    """
    Set the calendar events for use between classes
    :param data: The new calendar events data
    :return: None
    """
    global CALENDAR_EVENTS
    CALENDAR_EVENTS = data


def get_calendar_events():
    """
    Get the calendar events data
    :return: List of calendar events
    """
    return CALENDAR_EVENTS


def set_temperature(data):
    if data is not float or data < 0:
        raise Exception("The data provided to set the temperature was invalid. Expected float instead received: %s" % data)

    TEMPERATURE = data


def get_temperature():
    return TEMPERATURE

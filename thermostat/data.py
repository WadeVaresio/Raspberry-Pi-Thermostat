CALENDAR_EVENTS = []
TEMPERATURE = float


def set_calendar_events(data):
    """
    Set the calendar events for use between classes
    :param data: The new calendar events data
    :return: None
    """
    global CALENDAR_EVENTS

    if not isinstance(data, list):
        raise Exception("The data provided to set the calendar events was invalid. Expected a list but instead "
                        "received: %s" % str(type(data)))

    CALENDAR_EVENTS = data


def get_calendar_events():
    """
    Get the calendar events data
    :return: List of calendar events
    """
    return CALENDAR_EVENTS


def no_events():
    """
    Check to see if there are no upcoming events in the calendar
    :return: True if there are no upcoming events
    """
    return len(CALENDAR_EVENTS) == 0


def set_temperature(data):
    """
    Set the temperature. Raises exception if the data is not of type float.
    :param data: New temperature (float)
    :return: None
    """
    global TEMPERATURE

    if not isinstance(data, float):
        raise Exception("The data provided to set the temperature was invalid. Expected float instead received: %s"
                        % str(type(data)))

    TEMPERATURE = data


def get_temperature():
    """
    Get the temperature
    :return: Temperature (float)
    """
    return TEMPERATURE

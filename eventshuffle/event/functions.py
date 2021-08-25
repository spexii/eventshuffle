# Standard library imports
from datetime import datetime

def validate_dates(dates, event=None):
    """Checks the format of given dates (YYYY-MM-DD) and if the dates
    are valid.

    If event is going to be created (event argument is not given), there's
    a check that the dates are not in the past.
    
    If an existing event is given, check if the given dates are dates
    for the event.

    Args:
        dates (list): List of date strings
        event (Event, optional): An existing event. Defaults to None.

    Returns:
        str: An error message or empty string
    """
    # Get event dates for later check, if event is given
    event_dates = event.get_dates() if event else []

    # Check if dates are given in a list. If not, skip rest of the checking
    if type(dates) is not list or len(dates) == 0:
        return "A list of dates must be given!"

    for date_str in dates:
        # At first, try create a date object of the date string
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return f"Invalid date: {date_str}"

        # Check that date is not in the past, if event is not given
        if not event:
            if date_obj < datetime.now().date():
                return f"Date can't be in the past: {date_str}"
        # Otherwise, check if the date if one of the event dates
        else:
            if not date_obj in event_dates:
                return f"Date isn't one of the event dates: {date_str}"

    return ""

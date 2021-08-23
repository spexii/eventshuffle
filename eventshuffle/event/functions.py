# Standard library imports
from datetime import datetime

def validate_dates(dates):
    """Checks the format of given dates (YYYY-MM-DD) and that
    dates are not in the past.

    Args:
        dates (list): List of date strings

    Returns:
        str: An error message or empty string
    """
    # Check if dates are given in a list. If not, skip rest of the checking
    if not dates or type(dates) is not list or len(dates) == 0:
        return "A list of dates must be given!"

    for date_str in dates:
        # At first, try create a date object of the date string
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return f"Invalid date: {date_str}"

        # Check that date is not in the past
        if date_obj < datetime.now().date():
            return f"Date can't be in the past: {date_str}"

    return ""

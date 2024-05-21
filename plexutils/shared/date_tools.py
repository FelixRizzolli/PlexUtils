"""
This module contains utility functions for handling dates. It includes functions to check
if a given date is in the past or future.
"""

from datetime import datetime


def is_past_date(iso_date_string: str) -> bool:
    """
    Checks if the given ISO date string is a past date.

    Parameters:
        iso_date_string (str): The date string in ISO format.

    Returns:
        bool: True if the date is in the past, False otherwise.
    """
    return not is_future_date(iso_date_string)


def is_future_date(iso_date_string: str) -> bool:
    """
    Checks if the given ISO date string is a future date.

    Parameters:
        iso_date_string (str): The date string in ISO format.

    Returns:
        bool: True if the date is in the future, False otherwise.
    """
    # Parse the ISO date string into a datetime object
    date: datetime = datetime.fromisoformat(iso_date_string)

    # Get the current date and time
    now: datetime = datetime.now()

    # Compare the two dates
    if date > now:
        return True
    return False

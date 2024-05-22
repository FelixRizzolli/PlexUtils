"""
This module contains unit tests for the functions in the date_tools.py module.
"""

import unittest

from plexutils.shared.date_tools import is_future_date, is_past_date


class TestDateTools(unittest.TestCase):
    """
    This class contains unit tests for the functions in the date_tools.py module.
    """

    def test_is_past_date_with_past_date(self) -> None:
        """
        Test case for the `is_past_date` function when the input date is in the past.
        """
        date_to_check: str = "2000-01-01"
        self.assertTrue(is_past_date(date_to_check))

    def test_is_past_date_with_furure_date(self) -> None:
        """
        Test case for the `is_past_date` function when the input date is in the future.
        """
        date_to_check: str = "3000-01-01"
        self.assertFalse(is_past_date(date_to_check))

    def test_is_future_date_with_past_date(self) -> None:
        """
        Test case for the `is_future_date` function when the input date is in the past.
        """
        date_to_check: str = "2000-01-01"
        self.assertFalse(is_future_date(date_to_check))

    def test_is_future_date_with_furure_date(self) -> None:
        """
        Test case for the `is_future_date` function when the input date is in the future.
        """
        date_to_check: str = "3000-01-01"
        self.assertTrue(is_future_date(date_to_check))


if __name__ == "__main__":
    unittest.main()

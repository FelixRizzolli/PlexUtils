"""
This module contains the TestTVDBCredentials class which is used to test the
TVDBCredentials class.
"""

import unittest

from plexutils.config.tvdb_credentials import TVDBCredentials


class TestTVDBCredentials(unittest.TestCase):
    """
    Test case for the TVDBCredentials class.
    """

    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self.api_key = "test_api_key"
        self.api_pin = "test_api_pin"
        self.credentials = TVDBCredentials(self.api_key, self.api_pin)

    def test_initialization(self) -> None:
        """
        Test the initialization of the TVDBCredentials class.
        """
        self.assertEqual(self.credentials.api_key, self.api_key)
        self.assertEqual(self.credentials.api_pin, self.api_pin)

    def test_api_key_property(self) -> None:
        """
        Test the api_key property of the TVDBCredentials class.
        """
        self.assertEqual(self.credentials.api_key, self.api_key)

    def test_api_pin_property(self) -> None:
        """
        Test the api_pin property of the TVDBCredentials class.
        """
        self.assertEqual(self.credentials.api_pin, self.api_pin)


if __name__ == "__main__":
    unittest.main()

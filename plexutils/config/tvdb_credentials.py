"""
This module contains the TVDBCredentials class which is used to store and retrieve
TVDB API credentials.
"""

from dataclasses import dataclass


@dataclass
class TVDBCredentials:
    """
    A class used to represent TVDB API credentials.
    """

    api_key: str
    api_pin: str

    def to_dict(self) -> dict:
        """
        Convert the TVDBCredentials object to a dictionary.

        :return: A dictionary representation of the TVDBCredentials object.
        :rtype: dict
        """
        return {
            "api_key": self.api_key,
            "api_pin": self.api_pin,
        }

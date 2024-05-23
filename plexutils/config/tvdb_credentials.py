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

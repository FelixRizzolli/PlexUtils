"""
This module contains Movie class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.media_tools import extract_tvdbid


@dataclass
class Movie:
    """
    Represents a single movie.
    """

    def __init__(self, filename: str):
        self._filename: str = filename
        self._tvdbid: Optional[int] = extract_tvdbid(filename)

    @property
    def tvdbid(self) -> Optional[int]:
        """
        Returns the TVDB ID of the movie.

        :return: The TVDB ID of the movie.
        :rtype: Optional[int]
        """
        return self._tvdbid

    @property
    def filename(self) -> str:
        """
        Returns the filename of the movie.

        :return: The filename of the movie.
        :rtype: str
        """
        return self._filename

    def is_valid(self) -> bool:
        """
        Checks if the movie has a valid filename.

        :return: True if the movie has a valid filename, False otherwise.
        :rtype: bool
        """
        return self._tvdbid is not None

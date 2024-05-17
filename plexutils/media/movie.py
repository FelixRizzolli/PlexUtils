"""
This module contains Movie class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.utils import extract_tvdbid


@dataclass
class Movie:
    """
    Represents a single movie.

    Attributes:
        _filename (str): The filename of the movie.
        _tvdbid (Optional[int]): The TVDB ID of the movie.
    """

    def __init__(self, filename: str):
        self._filename: str = filename
        self._tvdbid: Optional[int] = extract_tvdbid(filename)

    @property
    def tvdbid(self) -> Optional[int]:
        """
        Returns the TVDB ID of the movie.

        Returns:
            Optional[int]: The TVDB ID of the movie.
        """
        return self._tvdbid

    @property
    def filename(self) -> str:
        """
        Returns the filename of the movie.

        Returns:
            str: The filename of the movie.
        """
        return self._filename

    def is_valid(self) -> bool:
        """
        Checks if the movie has a valid filename.

        Returns:
            bool: True if the movie has a valid filename, False otherwise.
        """
        return self._tvdbid is not None

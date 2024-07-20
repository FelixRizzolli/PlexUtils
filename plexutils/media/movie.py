"""
This module contains Movie class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.media_tools import extract_tvdbid
from plexutils.media.video_file import VideoFile


@dataclass
class Movie(VideoFile):
    """
    Represents a single movie.
    """

    @property
    def tvdbid(self) -> Optional[int]:
        """
        Returns the TVDB ID of the movie.

        :return: The TVDB ID of the movie.
        :rtype: Optional[int]
        """
        return extract_tvdbid(self._filename)

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
        return self.tvdbid is not None

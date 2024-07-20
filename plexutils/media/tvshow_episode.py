"""
This module contains TVShowEpisode class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.media_tools import (
    extract_episodeid,
    extract_seasonid_from_episode,
)


@dataclass
class TVShowEpisode:
    """
    Represents a single episode of a TV show.
    """

    def __init__(self, filename: str):
        self._filename: str = filename
        self._episode_id: Optional[int] = extract_episodeid(filename)

    @property
    def episode_id(self) -> Optional[int]:
        """
        Returns the ID of the episode.

        :return: The ID of the episode.
        :rtype: Optional[int]
        """
        return self._episode_id

    @property
    def filename(self) -> str:
        """
        Returns the filename of the episode.

        :return: The filename of the episode.
        :rtype: str
        """
        return self._filename

    def is_valid(self) -> bool:
        """
        Checks if the episode has a valid filename.

        :return: True if the episode has a valid filename, False otherwise.
        :rtype: bool
        """
        season_id: Optional[int] = extract_seasonid_from_episode(self._filename)
        return (self._episode_id is not None) and (season_id is not None)

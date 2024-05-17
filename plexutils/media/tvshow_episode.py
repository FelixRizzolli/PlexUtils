"""
This module contains TVShowEpisode class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.utils import extract_episodeid, extract_seasonid_from_episode


@dataclass
class TVShowEpisode:
    """
    Represents a single episode of a TV show.

    Attributes:
        _filename (str): The filename of the episode.
        _episode_id (Optional[int]): The ID of the episode.
    """

    def __init__(self, filename: str):
        self._filename: str = filename
        self._episode_id: Optional[int] = extract_episodeid(filename)

    @property
    def episode_id(self) -> Optional[int]:
        """
        Returns the ID of the episode.

        Returns:
            Optional[int]: The ID of the episode.
        """
        return self._episode_id

    @property
    def filename(self) -> str:
        """
        Returns the filename of the episode.

        Returns:
            str: The filename of the episode.
        """
        return self._filename

    def is_valid(self) -> bool:
        """
        Checks if the episode has a valid filename.

        Returns:
            bool: True if the episode has a valid filename, False otherwise.
        """
        season_id: Optional[int] = extract_seasonid_from_episode(self._filename)
        return (self._episode_id is not None) and (season_id is not None)

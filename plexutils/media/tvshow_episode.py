"""
This module contains TVShowEpisode class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.shared.media_tools import (
    extract_episodeid,
    extract_seasonid_from_episode,
)
from plexutils.media.video_file import VideoFile


@dataclass
class TVShowEpisode(VideoFile):
    """
    Represents a single episode of a TV show.
    """

    @property
    def episode_id(self) -> Optional[int]:
        """
        Returns the ID of the episode.

        :return: The ID of the episode.
        :rtype: Optional[int]
        """
        return extract_episodeid(self._filename)

    def is_valid(self) -> bool:
        """
        Checks if the episode has a valid filename.

        :return: True if the episode has a valid filename, False otherwise.
        :rtype: bool
        """
        season_id: Optional[int] = extract_seasonid_from_episode(self._filename)
        return (self.episode_id is not None) and (season_id is not None)

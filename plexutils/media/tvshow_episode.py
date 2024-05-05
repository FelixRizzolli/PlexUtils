"""
    This module contains TVShowList class.
"""
from typing import Optional

from plexutils.shared.utils import (
    extract_episodeid,
    extract_seasonid_from_episode
)


class TVShowEpisode:
    """represents a single episode of a tv show"""
    def __init__(self, filename: str):
        self.filename: str = filename
        self.episode_id: Optional[int] = extract_episodeid(filename)

    def get_id(self) -> Optional[int]:
        """returns the id of the episode"""
        return self.episode_id

    def is_valid(self) -> bool:
        """checks if the episode has a valid filename"""
        season_id: Optional[int] = extract_seasonid_from_episode(self.filename)
        return (self.episode_id is not None) and (season_id is not None)

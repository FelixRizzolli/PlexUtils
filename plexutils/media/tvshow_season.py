"""
This module contains TVShowSeason class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.shared.utils import extract_seasonid


@dataclass
class TVShowSeason:
    """
    Represents a single season of a TV show.

    Attributes:
        _dirname (str): The directory name of the season.
        _season_id (Optional[int]): The ID of the season.
        _episodes (dict[int, TVShowEpisode]): A dictionary mapping episode IDs to episodes.
    """

    def __init__(self, dirname: str):
        self._dirname: str = dirname
        self._season_id: Optional[int] = extract_seasonid(dirname)
        self._episodes: dict[int, TVShowEpisode] = {}

    @property
    def season_id(self) -> Optional[int]:
        """
        Returns the ID of the season.

        Returns:
            Optional[int]: The ID of the season.
        """
        return self._season_id

    @property
    def dirname(self) -> str:
        """
        Returns the directory name of the season.

        Returns:
            str: The directory name of the season.
        """
        return self._dirname

    @property
    def episodes(self) -> list[TVShowEpisode]:
        """
        Returns all the episodes of the season.

        Returns:
            list[TVShowEpisode]: A list of all episodes in the season.
        """
        return list(self._episodes.values())

    @property
    def episodeids(self) -> list[int]:
        """
        Returns all the episode IDs of the season.

        Returns:
            list[int]: A list of all episode IDs in the season.
        """
        return list(self._episodes.keys())

    def add_episode(self, episode: TVShowEpisode) -> None:
        """
        Adds an episode to the season.

        Args:
            episode (TVShowEpisode): The episode to add.
        """
        self._episodes[episode.episode_id] = episode

    def is_valid(self) -> bool:
        """
        Checks if the season's directory name is valid.

        Returns:
            bool: True if the season's directory name is valid, False otherwise.
        """
        return self._season_id is not None

    def is_empty(self) -> bool:
        """
        Checks if the season has no episodes.

        Returns:
            bool: True if the season has no episodes, False otherwise.
        """
        return len(self._episodes) == 0

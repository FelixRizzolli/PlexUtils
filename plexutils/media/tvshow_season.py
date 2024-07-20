"""
This module contains TVShowSeason class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.shared.media_tools import extract_seasonid


@dataclass
class TVShowSeason:
    """
    Represents a single season of a TV show.
    """

    def __init__(self, dirname: str):
        self._dirname: str = dirname
        self._season_id: Optional[int] = extract_seasonid(dirname)
        self._episodes: dict[int, TVShowEpisode] = {}

    @property
    def season_id(self) -> Optional[int]:
        """
        Returns the ID of the season.

        :return: The ID of the season.
        :rtype: Optional[int]
        """
        return self._season_id

    @property
    def dirname(self) -> str:
        """
        Returns the directory name of the season.

        :return: The directory name of the season.
        :rtype: str
        """
        return self._dirname

    @property
    def episodes(self) -> list[TVShowEpisode]:
        """
        Returns all the episodes of the season.

        :return: A list of all episodes in the season.
        :rtype: list[TVShowEpisode]
        """
        return list(self._episodes.values())

    @property
    def episodeids(self) -> list[int]:
        """
        Returns all the episode IDs of the season.

        :return: A list of all episode IDs in the season.
        :rtype: list[int]
        """
        return list(self._episodes.keys())

    def add_episode(self, episode: TVShowEpisode) -> None:
        """
        Adds an episode to the season.

        :param episode: The episode to add.
        :type episode: TVShowEpisode

        :return: None
        """
        if episode.episode_id is None:
            raise ValueError("Episode ID is required")
        if episode.episode_id in self._episodes:
            raise ValueError(f"Episode with ID {episode.episode_id} already exists")

        self._episodes[episode.episode_id] = episode

    def is_valid(self) -> bool:
        """
        Checks if the season's directory name is valid.

        :return: True if the season's directory name is valid, False otherwise.
        :rtype: bool
        """
        return self._season_id is not None

    def is_empty(self) -> bool:
        """
        Checks if the season has no episodes.

        :return: True if the season has no episodes, False otherwise.
        :rtype: bool
        """
        return len(self._episodes) == 0

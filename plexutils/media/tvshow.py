"""
This module contains TVShow class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.media_tools import extract_tvdbid


@dataclass
class TVShow:
    """
    Represents a single TV show.
    """

    def __init__(self, dirname: str):
        self._dirname: str = dirname
        self._tvdbid: Optional[int] = extract_tvdbid(dirname)
        self._seasons: dict[int, TVShowSeason] = {}

    @property
    def tvdbid(self) -> Optional[int]:
        """
        Returns the TVDB ID of the TV show.

        :return: The TVDB ID of the TV show.
        :rtype: Optional[int]
        """
        return self._tvdbid

    @property
    def dirname(self) -> str:
        """
        Returns the directory name of the TV show.

        :return: The directory name of the TV show.
        :rtype: str
        """
        return self._dirname

    @property
    def seasons(self) -> list[TVShowSeason]:
        """
        Returns the seasons of the TV show.

        :return: A list of the seasons of the TV show.
        :rtype: list[TVShowSeason]
        """
        return list(self._seasons.values())

    @property
    def seasonids(self) -> list[int]:
        """
        Returns the season IDs of the TV show.

        :return: A list of the season IDs of the TV show.
        :rtype: list[int]
        """
        return list(self._seasons.keys())

    def add_season(self, season: TVShowSeason) -> None:
        """
        Adds a season to the TV show.

        :param season: The season to add.
        :type season: TVShowSeason

        :return: None
        """
        if season.season_id is None:
            raise ValueError("Season ID is required")
        if season.season_id in self._seasons:
            raise ValueError(f"Season with ID {season.season_id} already exists")

        self._seasons[season.season_id] = season

    def get_season(self, season_id: int) -> Optional[TVShowSeason]:
        """
        Returns a season with the given ID of the TV show.

        :param season_id: The ID of the season to return.
        :type season_id: int

        :return: The season with the given ID, or None if no such season exists.
        :rtype: Optional[TVShowSeason]
        """
        return self._seasons.get(season_id)

    def is_valid(self) -> bool:
        """
        Checks if the TV show's directory name is valid.

        :return: True if the TV show's directory name is valid, False otherwise.
        :rtype: bool
        """
        return self._tvdbid is not None

    def is_empty(self) -> bool:
        """
        Checks if the TV show has any seasons.

        :return: True if the TV show has no seasons, False otherwise.
        :rtype: bool
        """
        return len(self._seasons) == 0

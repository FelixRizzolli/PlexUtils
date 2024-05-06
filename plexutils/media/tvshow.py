"""
This module contains TVShow class.
"""
from typing import Optional
from dataclasses import dataclass

from plexutils.shared.utils import extract_tvdbid
from plexutils.media.tvshow_season import TVShowSeason


@dataclass
class TVShow:
    """
    Represents a single TV show.

    Attributes:
        _dirname (str): The directory name of the TV show.
        _tvdbid (Optional[int]): The TVDB ID of the TV show.
        _seasons (dict[int, TVShowSeason]): A dictionary mapping season IDs to seasons.
    """

    def __init__(self, dirname: str):
        self._dirname: str = dirname
        self._tvdbid: Optional[int] = extract_tvdbid(dirname)
        self._seasons: dict[int, TVShowSeason] = {}

    @property
    def tvdbid(self) -> Optional[int]:
        """
        Returns the TVDB ID of the TV show.

        Returns:
            Optional[int]: The TVDB ID of the TV show.
        """
        return self._tvdbid

    @property
    def dirname(self) -> str:
        """
        Returns the directory name of the TV show.

        Returns:
            str: The directory name of the TV show.
        """
        return self._dirname

    def is_valid(self) -> bool:
        """
        Checks if the TV show's directory name is valid.

        Returns:
            bool: True if the TV show's directory name is valid, False otherwise.
        """
        return self._tvdbid is not None

    @property
    def seasons(self) -> list[TVShowSeason]:
        """
        Returns the seasons of the TV show.

        Returns:
            list[TVShowSeason]: A list of the seasons of the TV show.
        """
        return list(self._seasons.values())

    def get_seasonids(self) -> list[int]:
        """
        Returns the season IDs of the TV show.

        Returns:
            list[int]: A list of the season IDs of the TV show.
        """
        return list(self._seasons.keys())

    def add_season(self, season: TVShowSeason) -> None:
        """
        Adds a season to the TV show.

        Args:
            season (TVShowSeason): The season to add.
        """
        self._seasons[season.get_id()] = season

    def get_season(self, season_id: int) -> Optional[TVShowSeason]:
        """
        Returns a season with the given ID of the TV show.

        Args:
            season_id (int): The ID of the season to return.

        Returns:
            Optional[TVShowSeason]: The season with the given ID, or None if no such season exists.
        """
        return self._seasons.get(season_id)

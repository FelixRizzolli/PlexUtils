"""
This module contains TVShowList class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.media.tvshow import TVShow


@dataclass
class TVShowList:
    """
    Represents a collection of TV shows.

    Attributes:
        _tvshows (dict[int, TVShow]): A dictionary mapping TVDB IDs to TV shows.
    """

    def __init__(self):
        self._tvshows: dict[int, TVShow] = {}

    @property
    def tvshows(self) -> list[TVShow]:
        """
        Returns a collection of TV shows.

        Returns:
            list[TVShow]: A list of all TV shows in the collection.
        """
        return list(self._tvshows.values())

    def add_tvshow(self, tvshow: TVShow) -> None:
        """
        Adds a TV show to the list.

        Args:
            tvshow (TVShow): The TV show to add.
        """
        self._tvshows[tvshow.tvdbid] = tvshow

    def get_tvshow(self, tvshow_id: int) -> Optional[TVShow]:
        """
        Returns a TV show by ID.

        Args:
            tvshow_id (int): The TVDB ID of the TV show to return.

        Returns:
            Optional[TVShow]: The TV show with the given ID, or None if no such TV show exists.
        """
        return self._tvshows.get(tvshow_id)

    def is_empty(self) -> bool:
        """
        Checks if the collection is empty.

        Returns:
            bool: True if the collection is empty, False otherwise.
        """
        return len(self._tvshows) == 0

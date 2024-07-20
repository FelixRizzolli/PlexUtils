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
    """

    def __init__(self):
        self._tvshows: dict[int, TVShow] = {}

    @property
    def tvshows(self) -> list[TVShow]:
        """
        Returns a collection of TV shows.

        :return: A list of all TV shows in the collection.
        :rtype: list[TVShow]
        """
        return list(self._tvshows.values())

    def add_tvshow(self, tvshow: TVShow) -> None:
        """
        Adds a TV show to the list.

        :param tvshow: The TV show to add.
        :type tvshow: TVShow

        :raises ValueError: If the TV show TVDB ID is required or if a TV show with the same TVDB ID
                            already exists.

        :return: None
        """
        if tvshow.tvdbid is None:
            raise ValueError("TV show TVDB ID is required")
        if tvshow.tvdbid in self._tvshows:
            raise ValueError(f"TV show with TVDB ID {tvshow.tvdbid} already exists")

        self._tvshows[tvshow.tvdbid] = tvshow

    def get_tvshow(self, tvshow_id: int) -> Optional[TVShow]:
        """
        Returns a TV show by ID.

        :param tvshow_id: The TVDB ID of the TV show to return.
        :type tvshow_id: int

        :return: The TV show with the given ID, or None if no such TV show exists.
        :rtype: Optional[TVShow]
        """
        return self._tvshows.get(tvshow_id)

    def is_empty(self) -> bool:
        """
        Checks if the collection is empty.

        :return: True if the collection is empty, False otherwise.
        :rtype: bool
        """
        return len(self._tvshows) == 0

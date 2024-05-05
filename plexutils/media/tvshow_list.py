"""
    This module contains TVShowList class.
"""
from typing import Optional

from plexutils.media.tvshow import TVShow


class TVShowList:
    """represents a collection of tv shows"""
    def __init__(self):
        self.tvshows: list[TVShow] = []

    def add_tvshow(self, tvshow: TVShow) -> None:
        """adds a tv show to the list"""
        self.tvshows.append(tvshow)

    def get_tvshows(self) -> list[TVShow]:
        """returns a collection of tv shows"""
        return self.tvshows

    def get_tvshow(self, tvshow_id: int) -> Optional[TVShow]:
        """returns a tv show by id"""
        for tvshow in self.tvshows:
            if tvshow.get_tvdbid() == tvshow_id:
                return tvshow
        return None

    def is_empty(self) -> bool:
        """checks if collection is empty"""
        return len(self.tvshows) == 0

"""
    This module contains TVShow class.
"""
from typing import Optional

from plexutils.shared.utils import extract_tvdbid
from plexutils.media.tvshow_season import TVShowSeason


class TVShow:
    """represents a single tv show"""

    def __init__(self, dirname: str):
        self.dirname: str = dirname
        self.tvdbid: Optional[int] = extract_tvdbid(dirname)
        self.seasons: list[TVShowSeason] = []

    def get_tvdbid(self) -> Optional[int]:
        """returns the tvdbid of the tv show"""
        return self.tvdbid

    def get_dirname(self) -> str:
        """returns the directory name of the tv show"""
        return self.dirname

    def is_valid(self) -> bool:
        """checks if the tv shows directory name is valid"""
        return self.tvdbid is not None

    def get_seasons(self) -> list[TVShowSeason]:
        """returns the seasons of the tv show"""
        return self.seasons

    def get_seasonids(self) -> list[int]:
        """returns the season ids of the tv show"""
        ids: list[int] = []
        for season in self.seasons:
            ids.append(season.get_id())
        return ids

    def add_season(self, season: TVShowSeason) -> None:
        """adds a season to the tv show"""
        self.seasons.append(season)

    def get_season(self, season_id: int) -> Optional[TVShowSeason]:
        """returns a season with the given id of the tv show"""
        for season in self.seasons:
            if season.get_id() == season_id:
                return season
        return None

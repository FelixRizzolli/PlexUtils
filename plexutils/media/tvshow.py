"""
    This module contains TVShow class.
"""
from plexutils.shared.utils import extract_tvdbid


class TVShow:
    """represents a single tv show"""

    def __init__(self, dirname):
        self.dirname = dirname
        self.tvdbid = extract_tvdbid(dirname)
        self.seasons = []

    def get_tvdbid(self):
        """returns the tvdbid of the tv show"""
        return self.tvdbid

    def get_dirname(self):
        """returns the directory name of the tv show"""
        return self.dirname

    def is_valid(self):
        """checks if the tv shows directory name is valid"""
        return self.tvdbid is not None

    def get_seasons(self):
        """returns the seasons of the tv show"""
        return self.seasons

    def get_seasonids(self):
        """returns the season ids of the tv show"""
        ids = []
        for season in self.seasons:
            ids.append(season.get_id())
        return ids

    def add_season(self, season):
        """adds a season to the tv show"""
        self.seasons.append(season)

    def get_season(self, season_id):
        """returns a season with the given id of the tv show"""
        for season in self.seasons:
            if season.get_id() == season_id:
                return season
        return None

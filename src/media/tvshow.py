import re

from utils import extract_tvdbid


class TVShow:

    def __init__(self, dirname):
        self.dirname = dirname
        self.tvdbid = extract_tvdbid(dirname)
        self.seasons = []

    def get_tvdbid(self):
        return self.tvdbid

    def get_dirname(self):
        return self.dirname

    def is_valid(self):
        return self.tvdbid is not None

    def get_seasons(self):
        return self.seasons

    def add_season(self, season):
        self.seasons.append(season)
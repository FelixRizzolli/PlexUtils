import re

from utils import extract_tvdbid


class TVShow:

    def __init__(self, dirname):
        self.dirname = dirname
        self.tvdb_id = extract_tvdbid(dirname)
        self.seasons = []


    def get_tvdbid(self):
        return self.tvdbid


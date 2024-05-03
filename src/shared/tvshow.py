import re

from utils import extract_tvdbid


class TVShow:

    def __init__(self, dirname):
        self.dirname = dirname
        self.tvdbid = extract_tvdbid(dirname)
        self.seasons = []


    def get_tvdbid(self):
        return self.tvdbid


import re

tvdbid_pattern = r'{tvdb-(\d+)}'


class TVShow:

    def __init__(self, dirname):
        self.dirname = dirname
        self.tvdb_id = None
        self.seasons = []

        tvdbid_match = re.search(tvdbid_pattern, dirname)
        if tvdbid_match:
            self.tvdbid = int(tvdbid_match.group(1))

    def get_tvdbid(self):
        return self.tvdbid


from shared.utils import extract_tvdbid


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

    def get_seasonids(self):
        ids = []
        for season in self.seasons:
            ids.append(season.get_id())
        return ids

    def add_season(self, season):
        self.seasons.append(season)

    def get_season(self, season_id):
        for season in self.seasons:
            if season.get_id() == season_id:
                return season
        return None
from utils import extract_seasonid


class TVShowSeason:
    def __init__(self, tvshow_id, dirname):
        self.tvshow_id = tvshow_id
        self.season_id = extract_seasonid(dirname)
        self.dirname = dirname
        self.episodes = []


    def get_id(self):
        return self.season_id

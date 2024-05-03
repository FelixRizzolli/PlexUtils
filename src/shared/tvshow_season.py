from utils import extract_seasonid


class TVShowSeason:
    def __init__(self, dirname):
        self.season_id = extract_seasonid(dirname)
        self.dirname = dirname
        self.episodes = []


    def get_id(self):
        return self.season_id

from utils import extract_episodeid

class TVShowEpisode:
    def __init__(self, tvshow_id, season_id, filename):
        self.tvshow_id = tvshow_id
        self.season_id = season_id
        self.filename = filename
        self.episode_id = extract_episodeid(filename)


    def get_id(self):
        return self.episode_id
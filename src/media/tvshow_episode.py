from utils import extract_episodeid, extract_seasonid_from_episode


class TVShowEpisode:
    def __init__(self, filename):
        self.filename = filename
        self.episode_id = extract_episodeid(filename)

    def get_id(self):
        return self.episode_id

    def is_valid(self):
        season_id = extract_seasonid_from_episode(self.filename)
        return (self.episode_id is not None) and (season_id is not None)

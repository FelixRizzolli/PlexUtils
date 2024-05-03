from utils import extract_episodeid


class TVShowEpisode:
    def __init__(self, filename):
        self.filename = filename
        self.episode_id = extract_episodeid(filename)

    def get_id(self):
        return self.episode_id

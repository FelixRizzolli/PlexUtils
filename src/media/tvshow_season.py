from shared.utils import extract_seasonid


class TVShowSeason:
    def __init__(self, dirname):
        self.season_id = extract_seasonid(dirname)
        self.dirname = dirname
        self.episodes = []

    def get_id(self):
        return self.season_id

    def is_valid(self):
        return self.season_id is not None

    def get_episodes(self):
        return self.episodes

    def get_episodeids(self):
        ids = []
        for episode in self.episodes:
            ids.append(episode.get_id())
        return ids

    def add_episode(self, episode):
        self.episodes.append(episode)
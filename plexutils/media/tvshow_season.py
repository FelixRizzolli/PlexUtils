from plexutils.shared.utils import extract_seasonid


class TVShowSeason:
    """represents a single season of a tv show"""
    def __init__(self, dirname):
        self.season_id = extract_seasonid(dirname)
        self.dirname = dirname
        self.episodes = []

    def get_id(self):
        """returns the season id"""
        return self.season_id

    def is_valid(self):
        """checks if the seasons directory name is valid"""
        return self.season_id is not None

    def get_episodes(self):
        """returns all the episodes of the season"""
        return self.episodes

    def get_episodeids(self):
        """returns all the episode ids of the season"""
        ids = []
        for episode in self.episodes:
            ids.append(episode.get_id())
        return ids

    def add_episode(self, episode):
        """adds an episode to the season"""
        self.episodes.append(episode)

import re

episode_id_pattern = r'- s(\d+)e(\d+)'

class TVShowEpisode:
    def __init__(self, tvshow_id, season_id, filename):
        self.tvshow_id = tvshow_id
        self.season_id = season_id
        self.episode_id = None
        self.filename = filename

        episodeid_match = re.search(episode_id_pattern, filename)
        if episodeid_match:
            self.episode_id = int(episodeid_match.group(2))

    def get_id(self):
        return self.episode_id
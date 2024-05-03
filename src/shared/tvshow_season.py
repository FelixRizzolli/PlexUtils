import re

season_id_pattern = r'season (\d+)'


class TVShowSeason:
    def __init__(self, tvshow_id, dirname):
        self.tvshow_id = tvshow_id
        self.season_id = None
        self.dirname = dirname
        self.episodes = []

        seasonid_match = re.search(season_id_pattern, dirname)
        if seasonid_match:
            self.season_id = int(seasonid_match.group(1))

    def get_id(self):
        return self.season_id

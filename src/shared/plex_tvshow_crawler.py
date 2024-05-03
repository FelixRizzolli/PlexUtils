import os
import re

tvdb_id_pattern = r'{tvdb-(\d+)}'
season_id_pattern = r'season (\d+)'


def crawl_seasons(directory):
    season_directories = os.listdir(directory)

    seasons = []

    for seasons_directory in season_directories:
        match = re.search(season_id_pattern, seasons_directory)
        if match:
            season = {
                "id": int(match.group(1)),
                "dirname": seasons_directory,
            }
            seasons.append(season)

    return seasons


class PlexTvshowCrawler(object):
    def __init__(self, path):
        self.invalid_tvshows = None
        self.invalid_seasons = None
        self.invalid_episodes = None
        self.tvshows = None
        self.path = path

    def crawl(self):
        directories = os.listdir(self.path)

        self.tvshows = []
        self.invalid_tvshows = []

        for directory in directories:
            match = re.search(tvdb_id_pattern, directory)
            if match:
                tvshow = {
                    "id": match.group(1),
                    "dirname": directory,
                    "seasons": crawl_seasons(os.path.join(self.path, directory))
                }
                self.tvshows.append(tvshow)
            else:
                self.invalid_tvshows.append(directory)

    def get_tvshows(self):
        return self.tvshows

    def get_seasons(self, tvshow_id):
        tvshow = list(filter(lambda tvshow: tvshow["id"] == tvshow_id, self.tvshows))[0]
        return tvshow["seasons"]

    def get_episodes(self, tvshow_id, season_id):
        return []

    def get_invalid_tvshows(self):
        return self.invalid_tvshows

    def get_invalid_seasons(self):
        return self.invalid_seasons

    def get_invalid_episodes(self):
        return self.invalid_episodes

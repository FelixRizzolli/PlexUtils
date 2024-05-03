import os
import re

tvdb_id_pattern = r'{tvdb-(\d+)}'

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
                }
                self.tvshows.append(tvshow)
            else:
                self.invalid_tvshows.append(directory)

    def get_tvshows(self):
        return self.tvshows

    def get_seasons(self, tvshow_id):
        return []

    def get_episodes(self, tvshow_id, season_id):
        return []

    def get_invalid_tvshows(self):
        return self.invalid_tvshows

    def get_invalid_seasons(self):
        return self.invalid_seasons

    def get_invalid_episodes(self):
        return self.invalid_episodes

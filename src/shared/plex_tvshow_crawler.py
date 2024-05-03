import json
import os
import re

tvdb_id_pattern = r'{tvdb-(\d+)}'
season_id_pattern = r'season (\d+)'
episode_id_pattern = r'- s(\d+)e(\d+)'


def crawl_seasons(tvshow_directory):
    season_directories = os.listdir(tvshow_directory)

    seasons = []

    for season_dirname in season_directories:
        match = re.search(season_id_pattern, season_dirname)
        if match:
            season = {
                "id": int(match.group(1)),
                "dirname": season_dirname,
                "episodes": crawl_episodes(os.path.join(tvshow_directory, season_dirname))
            }
            seasons.append(season)

    return seasons


def crawl_episodes(directory):
    episode_directories = os.listdir(directory)

    episodes = []

    for episode_filename in episode_directories:
        match = re.search(episode_id_pattern, episode_filename)
        if match:
            episode = {
                "id": int(match.group(2)),
                "filename": episode_filename,
            }
            episodes.append(episode)

    return episodes


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
        tvshow = list(filter(lambda tvshow: tvshow["id"] == tvshow_id, self.tvshows))[0]
        season = list(filter(lambda season: season["id"] == season_id, tvshow["seasons"]))[0]
        return season["episodes"]

    def get_invalid_tvshows(self):
        return self.invalid_tvshows

    def get_invalid_seasons(self):
        return self.invalid_seasons

    def get_invalid_episodes(self):
        return self.invalid_episodes

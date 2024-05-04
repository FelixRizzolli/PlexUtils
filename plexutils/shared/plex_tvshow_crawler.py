import os

from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.media.tvshow_episode import TVShowEpisode

class PlexTvshowCrawler(object):
    def __init__(self, path):
        self.invalid_tvshows = None
        self.invalid_seasons = None
        self.invalid_episodes = None
        self.tvshowlist = TVShowList()
        self.path = path

    def crawl(self):
        tvshow_directories = os.listdir(self.path)

        self.invalid_tvshows = []
        self.invalid_seasons = []
        self.invalid_episodes = []

        for tvshow_dir in tvshow_directories:
            tvshow = TVShow(tvshow_dir)

            seasons = self.crawl_seasons(tvshow_dir)
            for season in seasons:
                tvshow.add_season(season)

            if tvshow.is_valid():
                self.tvshowlist.add_tvshow(tvshow)
            else:
                self.invalid_tvshows.append(f"{tvshow_dir}")

    def crawl_seasons(self, tvshow_dir):
        seasons = []
        season_directories = os.listdir(os.path.join(self.path, tvshow_dir))

        for season_dir in season_directories:
            season = TVShowSeason(season_dir)

            episodes = self.crawl_episodes(tvshow_dir, season_dir)
            for episode in episodes:
                season.add_episode(episode)

            if season.is_valid():
                seasons.append(season)
            else:
                self.invalid_seasons.append(f"{tvshow_dir} -> {season_dir}")

        return seasons

    def crawl_episodes(self, tvshow_dir, season_dir):
        episodes = []
        episode_directories = os.listdir(os.path.join(self.path, tvshow_dir, season_dir))

        for episode_dir in episode_directories:
            episode = TVShowEpisode(episode_dir)

            if episode.is_valid():
                episodes.append(episode)
            else:
                self.invalid_episodes.append(f"{tvshow_dir} -> {season_dir} -> {episode_dir}")

        return episodes

    def get_tvshowlist(self):
        return self.tvshowlist

    def get_invalid_tvshows(self):
        return self.invalid_tvshows

    def get_invalid_seasons(self):
        return self.invalid_seasons

    def get_invalid_episodes(self):
        return self.invalid_episodes

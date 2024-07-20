"""
    This module contains PlexTvshowCrawler class.
"""

import os

from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow_season import TVShowSeason


class PlexTVShowCrawler:
    """
    class for crawling tvshow data from a plex library
    """

    def __init__(self, path):
        self.invalid_tvshows: list[str] = []
        self.invalid_seasons: list[str] = []
        self.invalid_episodes: list[str] = []
        self.tvshowlist = TVShowList()
        self.path = path

    def crawl(self) -> None:
        """
        crawls the tvshows from a plex library

        :return: None
        """
        tvshow_directories: list[str] = os.listdir(self.path)

        for tvshow_dir in tvshow_directories:
            tvshow: TVShow = TVShow(tvshow_dir)

            seasons: list[TVShowSeason] = self.crawl_seasons(tvshow_dir)
            for season in seasons:
                tvshow.add_season(season)

            if tvshow.is_valid():
                self.tvshowlist.add_tvshow(tvshow)
            else:
                self.invalid_tvshows.append(f"{tvshow_dir}")

    def crawl_seasons(self, tvshow_dir: str) -> list[TVShowSeason]:
        """
        crawls the seasons from the given tvshow directory

        :param tvshow_dir: The directory of the tvshow
        :type tvshow_dir: str

        :return: A list of seasons
        :rtype: list[TVShowSeason]
        """
        seasons: list[TVShowSeason] = []
        season_directories: list[str] = os.listdir(os.path.join(self.path, tvshow_dir))

        for season_dir in season_directories:
            season: TVShowSeason = TVShowSeason(season_dir)

            episodes: list[TVShowEpisode] = self.crawl_episodes(tvshow_dir, season_dir)
            for episode in episodes:
                season.add_episode(episode)

            if season.is_valid():
                seasons.append(season)
            else:
                self.invalid_seasons.append(f"{tvshow_dir} -> {season_dir}")

        return seasons

    def crawl_episodes(self, tvshow_dir: str, season_dir: str) -> list[TVShowEpisode]:
        """
        crawls the episodes from the given tvshow and season directory

        :param tvshow_dir: The directory of the tvshow
        :type tvshow_dir: str
        :param season_dir: The directory of the season
        :type season_dir: str

        :return: A list of episodes
        :rtype: list[TVShowEpisode]
        """
        episodes: list[TVShowEpisode] = []
        episode_directories: list[str] = os.listdir(
            os.path.join(self.path, tvshow_dir, season_dir)
        )

        for episode_dir in episode_directories:
            episode: TVShowEpisode = TVShowEpisode(episode_dir)

            if episode.is_valid():
                episodes.append(episode)
            else:
                self.invalid_episodes.append(
                    f"{tvshow_dir} -> {season_dir} -> {episode_dir}"
                )

        return episodes

    def get_tvshowlist(self) -> TVShowList:
        """
        returns the list of all tvshows

        :return: The list of all tvshows
        :rtype: TVShowList
        """
        return self.tvshowlist

    def get_invalid_tvshows(self) -> list[str]:
        """
        returns the list of invalid tvshows

        :return: The list of invalid tvshows
        :rtype: list[str]
        """
        return self.invalid_tvshows

    def get_invalid_seasons(self) -> list[str]:
        """
        returns the list of invalid seasons

        :return: The list of invalid seasons
        :rtype: list[str]
        """
        return self.invalid_seasons

    def get_invalid_episodes(self) -> list[str]:
        """
        returns the list of invalid episodes

        :return: The list of invalid episodes
        :rtype: list[str]
        """
        return self.invalid_episodes

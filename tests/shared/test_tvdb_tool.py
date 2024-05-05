"""
    This module contains unit tests for the TVDBTool class.
"""
import unittest
import os
from typing import Set

from plexutils.shared.plex_tvshow_crawler import PlexTvshowCrawler
from plexutils.shared.utils import load_config
from plexutils.shared.tvdb_tool import TVDBTool

from tests.testdata import test_tvshow_files
from tvshow_episode import TVShowEpisode
from tvshow_season import TVShowSeason

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')


class TestTVDBTool(unittest.TestCase):
    """test class for the TVDBTool class"""

    def setUp(self) -> None:
        self.tvshow_directories: list[dict] = test_tvshow_files
        self.config: dict = load_config(os.path.join(current_script_dir, '../../config.yaml'))

        # initialize crawler
        self.crawler: PlexTvshowCrawler = PlexTvshowCrawler(tvshows_dir)
        self.crawler.crawl()
        if self.crawler.get_tvshowlist().is_empty():
            print("EMPTY TV SHOWS")

    def test_get_episodes(self) -> None:
        """test the get_episodes method"""
        tvdb_tool: TVDBTool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_episodes: list[dict] = tvdb_tool.get_episodes(121361, 1)
        plex_got_episodes: list[TVShowEpisode] = (self.crawler.get_tvshowlist()
                                                  .get_tvshow(121361)
                                                  .get_season(1)
                                                  .get_episodes())

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))

    def test_get_seasons(self) -> None:
        """test the get_seasons method"""
        tvdb_tool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_seasons: Set[int] = tvdb_tool.get_seasonids(121361)
        plex_got_seasons: list[TVShowSeason] = (self.crawler.get_tvshowlist()
                                                .get_tvshow(121361)
                                                .get_seasons())

        self.assertEqual(len(tvdb_got_seasons), len(plex_got_seasons))

    def test_get_episodeids(self) -> None:
        """test the get_episodeids method"""
        tvdb_tool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_episodes: Set[int] = tvdb_tool.get_episodeids(121361, 1)
        plex_got_episodes: list[TVShowEpisode] = (self.crawler.get_tvshowlist()
                                                  .get_tvshow(121361)
                                                  .get_season(1)
                                                  .get_episodes())

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))


if __name__ == '__main__':
    unittest.main()

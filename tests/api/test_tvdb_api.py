"""
    This module contains unit tests for the TVDBTool class.
"""

import os
import unittest

from plexutils.api.tvdb_api import TvdbApi
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.utils import load_config


class TestTvdbApi(unittest.TestCase):
    """test class for the TVDBTool class"""

    @classmethod
    def setUpClass(cls) -> None:
        # Define directory paths
        current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
        data_dir: str = os.path.join(current_script_dir, "../../data")
        tvshows_dir: str = os.path.join(data_dir, "tvshows")

        # Load congig.yaml
        cls.config: dict = load_config(
            os.path.join(current_script_dir, "../../config.yaml")
        )

        # Initialize crawler
        cls.crawler: PlexTVShowCrawler = PlexTVShowCrawler(tvshows_dir)
        cls.crawler.crawl()

    def test_get_episodes(self) -> None:
        """test the get_episodes method"""
        tvdb_tool: TvdbApi = TvdbApi(self.config["tvdb-key"], self.config["tvdb-pin"])
        tvdb_got_episodes: list[dict] = tvdb_tool.get_episodes(121361, 1)
        plex_got_episodes: list[TVShowEpisode] = (
            self.crawler.get_tvshowlist().get_tvshow(121361).get_season(1).episodes
        )

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))

    def test_get_seasons(self) -> None:
        """test the get_seasons method"""
        tvdb_tool = TvdbApi(self.config["tvdb-key"], self.config["tvdb-pin"])
        tvdb_got_seasons: set[int] = tvdb_tool.get_seasonids(121361)
        plex_got_seasons: list[TVShowSeason] = (
            self.crawler.get_tvshowlist().get_tvshow(121361).seasons
        )

        self.assertEqual(len(tvdb_got_seasons), len(plex_got_seasons))

    def test_get_episodeids(self) -> None:
        """test the get_episodeids method"""
        tvdb_tool = TvdbApi(self.config["tvdb-key"], self.config["tvdb-pin"])
        tvdb_got_episodes: set[int] = tvdb_tool.get_episodeids(121361, 1)
        plex_got_episodes: list[TVShowEpisode] = (
            self.crawler.get_tvshowlist().get_tvshow(121361).get_season(1).episodes
        )

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))


if __name__ == "__main__":
    unittest.main()

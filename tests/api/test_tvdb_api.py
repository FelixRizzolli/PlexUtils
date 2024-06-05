"""
    This module contains unit tests for the TVDBTool class.
"""

import os
import unittest
from typing import Optional

from plexutils.api.tvdb_api import TvdbApi
from plexutils.config.config import Config
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.config_tools import load_config_from_file


class TestTvdbApi(unittest.TestCase):
    """test class for the TVDBTool class"""

    config: Config
    crawler: PlexTVShowCrawler

    @classmethod
    def setUpClass(cls) -> None:
        # Define directory paths
        current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(current_script_dir, "..", "..")
        data_dir: str = os.path.join(pj_path, "data")
        tvshows_dir: str = os.path.join(data_dir, "tvshows", "tvshows")

        # Load congig.yaml
        config_file: str = os.path.join(pj_path, "config.yaml")
        cls.config = load_config_from_file(config_file)

        # Initialize crawler
        cls.crawler = PlexTVShowCrawler(tvshows_dir)
        cls.crawler.crawl()

    def test_get_episodes(self) -> None:
        """test the get_episodes method"""
        tvdb_tool: TvdbApi = TvdbApi(self.config.tvdb.api_key, self.config.tvdb.api_pin)
        tvdb_got_episodes: list[dict] = tvdb_tool.get_episodes(121361, 1)

        tvshowlist: TVShowList = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            tvshow: Optional[TVShow] = tvshowlist.get_tvshow(121361)
            if tvshow is not None:
                plex_got_season_1: Optional[TVShowSeason] = tvshow.get_season(1)
                if plex_got_season_1 is not None:
                    plex_got_episodes: list[TVShowEpisode] = plex_got_season_1.episodes
                    self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))

    def test_get_seasons(self) -> None:
        """test the get_seasons method"""
        tvdb_tool = TvdbApi(self.config.tvdb.api_key, self.config.tvdb.api_pin)
        tvdb_got_seasons: set[int] = tvdb_tool.get_seasonids(121361)

        tvshowlist: TVShowList = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            tvshow: Optional[TVShow] = tvshowlist.get_tvshow(121361)
            if tvshow is not None:
                plex_got_seasons: list[TVShowSeason] = tvshow.seasons
                self.assertEqual(len(tvdb_got_seasons), len(plex_got_seasons))

    def test_get_episodeids(self) -> None:
        """test the get_episodeids method"""
        tvdb_tool = TvdbApi(self.config.tvdb.api_key, self.config.tvdb.api_pin)
        tvdb_got_episodes: set[int] = tvdb_tool.get_episodeids(121361, 1)

        tvshowlist: TVShowList = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            tvshow: Optional[TVShow] = tvshowlist.get_tvshow(121361)
            if tvshow is not None:
                plex_got_season_1: Optional[TVShowSeason] = tvshow.get_season(1)
                if plex_got_season_1 is not None:
                    plex_got_episodes: list[TVShowEpisode] = plex_got_season_1.episodes
                    plex_got_episodeids: set[Optional[int]] = {
                        episode.episode_id for episode in plex_got_episodes
                    }
                    self.assertEqual(tvdb_got_episodes, plex_got_episodeids)


if __name__ == "__main__":
    unittest.main()

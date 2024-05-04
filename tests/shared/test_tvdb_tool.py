import json
import unittest
import os
import yaml

from plex_tvshow_crawler import PlexTvshowCrawler
from test_data import test_tvshow_files

from utils import load_config
from tvdb_tool import TVDBTool

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')


class TestTVDBTool(unittest.TestCase):

    def setUp(self):
        self.tvshow_directories = test_tvshow_files
        self.config = load_config(os.path.join(current_script_dir, '../../config.yaml'))

        # initialize crawler
        self.crawler = PlexTvshowCrawler(tvshows_dir)
        self.crawler.crawl()
        if self.crawler.get_tvshowlist().is_empty():
            print("EMPTY TV SHOWS")

    def test_get_episodes(self):
        tvdb_tool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_episodes = tvdb_tool.get_episodes(121361, 1)
        plex_got_episodes = self.crawler.get_tvshowlist().get_tvshow(121361).get_season(1).get_episodes()

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))

    def test_get_seasons(self):
        tvdb_tool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_seasons = tvdb_tool.get_seasonids(121361)
        plex_got_seasons = self.crawler.get_tvshowlist().get_tvshow(121361).get_seasons()

        self.assertEqual(len(tvdb_got_seasons), len(plex_got_seasons))


if __name__ == '__main__':
    unittest.main()

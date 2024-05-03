import json
import unittest
import os
import yaml

from plex_tvshow_crawler import PlexTvshowCrawler
from test_data import test_tvshow_files

from utils import delete_directory, load_config
from tvdb_tool import TVDBTool

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')


class TestTVDBTool(unittest.TestCase):

    def setUp(self):
        self.tvshow_directories = test_tvshow_files
        self.config = load_config(os.path.join(current_script_dir, '../../config.yaml'))

        # clear data
        if os.path.isdir(tvshows_dir):
            delete_directory(tvshows_dir)

        # create data
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(tvshows_dir):
            os.mkdir(tvshows_dir)

        for tvshow in self.tvshow_directories:
            tvshow_dirname = tvshow["dirname"]
            tvshow_dir = os.path.join(tvshows_dir, tvshow_dirname)
            if not os.path.isdir(tvshow_dir):
                os.mkdir(tvshow_dir)

            for season in tvshow["seasons"]:
                season_dirname = season["dirname"]
                season_dir = os.path.join(tvshow_dir, season_dirname)
                if not os.path.isdir(season_dir):
                    os.mkdir(season_dir)

                for episode in season["episodes"]:
                    episode_dir = os.path.join(season_dir, episode)
                    open(episode_dir, 'a').close()

        # initialize crawler
        self.crawler = PlexTvshowCrawler(tvshows_dir)
        self.crawler.crawl()
        if self.crawler.get_tvshowlist().is_empty():
            print("EMPTY TV SHOWS")

    def test_get_episodes(self):
        print(json.dumps(self.config, indent=4))
        tvdb_tool = TVDBTool(self.config['tvdb-key'], self.config['tvdb-pin'])
        tvdb_got_episodes = tvdb_tool.get_episodes(121361, 1)
        plex_got_episodes = self.crawler.get_tvshowlist().get_tvshow(121361).get_season(1).get_episodes()

        self.assertEqual(len(tvdb_got_episodes), len(plex_got_episodes))


if __name__ == '__main__':
    unittest.main()

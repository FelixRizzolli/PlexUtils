import json
import unittest
import os

from plex_tvshow_crawler import PlexTvshowCrawler
from test_data import test_tvshow_files

from utils import delete_directory

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')


class TestPlexTvshowsCrawler(unittest.TestCase):

    def setUp(self):
        self.tvshow_directories = test_tvshow_files

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

    def test_crawl_get_tvshows_count(self):
        tvshows = self.crawler.get_tvshows()
        invalid_tvshows = self.crawler.get_invalid_tvshows()
        self.assertEqual(len(self.tvshow_directories), len(tvshows) + len(invalid_tvshows))

    def test_crawl_get_tvshows_object(self):
        tvshows = self.crawler.get_tvshows()
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", tvshows))[0]
        self.assertEqual(codegeass["dirname"], "Code Geass (2006) {tvdb-79525}")
        self.assertEqual(codegeass["id"], "79525")

    def test_crawl_get_invalid_tvshows(self):
        invalid_tvshows = self.crawler.get_invalid_tvshows()
        self.assertEqual("Classroom of the Elite (2017)", invalid_tvshows[0])

    def test_crawl_get_seasons_count(self):
        seasons = self.crawler.get_seasons("79525")
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", self.tvshow_directories))[0]
        self.assertEqual(len(codegeass["seasons"]), len(seasons))

    def test_crawl_get_episodes_count(self):
        episodes = self.crawler.get_episodes("79525", 1)
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", self.tvshow_directories))[0]
        season1 = list(filter(lambda season: season["dirname"] == "season 01", codegeass["seasons"]))[0]
        self.assertEqual(len(season1["episodes"]), len(episodes))


if __name__ == '__main__':
    unittest.main()

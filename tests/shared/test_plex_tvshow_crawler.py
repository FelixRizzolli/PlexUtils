import json
import unittest
import os

from plex_tvshow_crawler import PlexTvshowCrawler
from test_data import test_tvshow_files

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')


class TestPlexTvshowsCrawler(unittest.TestCase):

    def setUp(self):
        self.tvshow_directories = test_tvshow_files

        # initialize crawler
        self.crawler = PlexTvshowCrawler(tvshows_dir)
        self.crawler.crawl()
        if self.crawler.get_tvshowlist().is_empty():
            print("EMPTY TV SHOWS")

    def test_crawl_get_tvshows_count(self):
        tvshows = self.crawler.get_tvshowlist().get_tvshows()
        invalid_tvshows = self.crawler.get_invalid_tvshows()
        self.assertEqual(len(self.tvshow_directories), len(tvshows) + len(invalid_tvshows))

    def test_crawl_get_tvshows_object(self):
        tvshowlist = self.crawler.get_tvshowlist()
        codegeass = tvshowlist.get_tvshow(79525)
        self.assertEqual(codegeass.get_dirname(), "Code Geass (2006) {tvdb-79525}")
        self.assertEqual(codegeass.get_tvdbid(), 79525)

    def test_crawl_get_invalid_tvshows(self):
        invalid_tvshows = self.crawler.get_invalid_tvshows()
        self.assertEqual("Classroom of the Elite (2017)", invalid_tvshows[0])

    def test_crawl_get_seasons_count(self):
        seasons = self.crawler.get_tvshowlist().get_tvshow(79525).get_seasons()
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", self.tvshow_directories))[0]
        self.assertEqual(len(codegeass["seasons"]), len(seasons))

    def test_crawl_get_episodes_count(self):
        episodes = self.crawler.get_tvshowlist().get_tvshow(79525).get_season(1).get_episodes()
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", self.tvshow_directories))[0]
        season1 = list(filter(lambda season: season["dirname"] == "season 01", codegeass["seasons"]))[0]
        self.assertEqual(len(season1["episodes"]), len(episodes))


if __name__ == '__main__':
    unittest.main()

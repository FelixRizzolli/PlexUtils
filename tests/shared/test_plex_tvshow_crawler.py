import unittest
import os

from plex_tvshow_crawler import PlexTvshowCrawler

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
tvshows_dir = os.path.join(data_dir, 'tvshows')

class TestPlexTvshowsCrawler(unittest.TestCase):

    def setUp(self):
        self.tvshow_directories = [
            "Game of Thrones (2011) {tvdb-121361}",
            "Money Heist (2017) {tvdb-327417}",
            "My Name (2021) {tvdb-397441}",
            "Code Geass (2006) {tvdb-79525}",
        ]

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(tvshows_dir):
            os.mkdir(tvshows_dir)

        for tvshow_directory in self.tvshow_directories:
            if not os.path.isdir(os.path.join(tvshows_dir, tvshow_directory)):
                os.mkdir(os.path.join(tvshows_dir, tvshow_directory))

        self.crawler = PlexTvshowCrawler(tvshows_dir)
        self.crawler.crawl()

    def test_crawl_get_tvshows_count(self):
        tvshows = self.crawler.get_tvshows()
        self.assertEqual(len(self.tvshow_directories), len(tvshows))

    def test_crawl_get_tvshows_object(self):
        tvshows = self.crawler.get_tvshows()
        codegeass = list(filter(lambda tvshow: tvshow["dirname"] == "Code Geass (2006) {tvdb-79525}", tvshows))[0]
        self.assertEqual(codegeass["dirname"], "Code Geass (2006) {tvdb-79525}")
        self.assertEqual(codegeass["id"], "79525")


if __name__ == '__main__':
    unittest.main()

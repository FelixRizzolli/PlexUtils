"""
    This module contains unit tests for the TestPlexMovieCrawler class.
"""
import unittest
import os

from plexutils.shared.plex_movie_crawler import PlexMovieCrawler
from tests.testdata import test_movie_files

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
movies_dir = os.path.join(data_dir, 'movies')


class TestPlexMovieCrawler(unittest.TestCase):
    """test class for the PlexMovieCrawler class"""

    def setUp(self):
        self.movie_files = test_movie_files

        # initialize crawler
        self.crawler = PlexMovieCrawler(movies_dir)
        self.crawler.crawl()

    def test_crawl_get_movies_count(self):
        """
            tests the get_movies method
                by counting the number of movies
                and comparing the result with the expected number of movies
        """
        movielist = self.crawler.get_movielist()
        invalid_movies = self.crawler.get_invalid_movies()
        self.assertEqual(len(self.movie_files), len(movielist.get_movies()) + len(invalid_movies))

    def test_crawl_get_movies_object(self):
        """
            tests the get_movies method
                by selecting a specific movie
                and comparing the result with the expected data
        """
        movielist = self.crawler.get_movielist()
        matrix1 = movielist.get_movie(169)
        self.assertEqual(matrix1.get_filename(), "The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(matrix1.get_tvdbid(), 169)

    def test_crawl_get_invalid_movies(self):
        """
            tests the get_invalid_movies method
                by selecting the first element in the collection
                and comparing the result with the expected data
        """
        invalid_movies = self.crawler.get_invalid_movies()
        self.assertEqual("Baby Driver (2017).mp4", invalid_movies[0])


if __name__ == '__main__':
    unittest.main()

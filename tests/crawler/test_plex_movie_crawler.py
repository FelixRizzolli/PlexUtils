"""
    This module contains unit tests for the TestPlexMovieCrawler class.
"""
import unittest
import os

from plexutils.media.movie import Movie
from plexutils.media.movie_list import MovieList
from plexutils.crawler.plex_movie_crawler import PlexMovieCrawler

from tests.testdata import test_movie_files

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
movies_dir = os.path.join(data_dir, 'movies')


class TestPlexMovieCrawler(unittest.TestCase):
    """test class for the PlexMovieCrawler class"""

    def setUp(self) -> None:
        self.movie_files: list[str] = test_movie_files

        # initialize crawler
        self.crawler: PlexMovieCrawler = PlexMovieCrawler(movies_dir)
        self.crawler.crawl()

    def test_crawl_get_movies_count(self) -> None:
        """
            tests the get_movies method
                by counting the number of movies
                and comparing the result with the expected number of movies
        """
        movielist: MovieList = self.crawler.get_movielist()
        invalid_movies: list[str] = self.crawler.get_invalid_movies()
        self.assertEqual(len(self.movie_files), len(movielist.movies) + len(invalid_movies))

    def test_crawl_get_movies_object(self) -> None:
        """
            tests the get_movies method
                by selecting a specific movie
                and comparing the result with the expected data
        """
        movielist: MovieList = self.crawler.get_movielist()
        matrix1: Movie = movielist.get_movie(169)
        self.assertEqual(matrix1.filename, "The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(matrix1.tvdbid, 169)

    def test_crawl_get_invalid_movies(self) -> None:
        """
            tests the get_invalid_movies method
                by selecting the first element in the collection
                and comparing the result with the expected data
        """
        invalid_movies: list[str] = self.crawler.get_invalid_movies()
        self.assertEqual("Baby Driver (2017).mp4", invalid_movies[0])


if __name__ == '__main__':
    unittest.main()

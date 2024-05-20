"""
    This module contains unit tests for the TestPlexMovieCrawler class.
"""

import json
import os
import unittest

from plexutils.crawler.plex_movie_crawler import PlexMovieCrawler
from plexutils.media.movie import Movie
from plexutils.media.movie_list import MovieList


class TestPlexMovieCrawler(unittest.TestCase):
    """test class for the PlexMovieCrawler class"""

    config: dict = {}
    crawler: PlexMovieCrawler = None

    @classmethod
    def setUpClass(cls) -> None:
        # Define directory paths
        current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
        data_dir: str = os.path.join(current_script_dir, "../../data")
        scripts_data_dir: str = os.path.join(current_script_dir, "../../scripts/data")
        movies_dir: str = os.path.join(data_dir, "movies", "movies")

        # Open the JSON file
        movies_data_file = os.path.join(scripts_data_dir, "movies", "movie_files.json")
        with open(movies_data_file, "r", encoding="utf-8") as f:
            # Load the JSON data into a Python dictionary
            cls.movie_files: dict = json.load(f)["movie_files"]

        # Initialize crawler
        cls.crawler: PlexMovieCrawler = PlexMovieCrawler(movies_dir)
        cls.crawler.crawl()

    def test_crawl_get_movies_count(self) -> None:
        """
        tests the get_movies method
            by counting the number of movies
            and comparing the result with the expected number of movies
        """
        movielist: MovieList = self.crawler.get_movielist()
        invalid_movies: list[str] = self.crawler.get_invalid_movies()
        self.assertEqual(
            len(self.movie_files), len(movielist.movies) + len(invalid_movies)
        )

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
        self.assertIn("Baby Driver (2017).mp4", invalid_movies)


if __name__ == "__main__":
    unittest.main()

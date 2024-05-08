"""
    This module contains unit tests for the MovieList class.
"""
import unittest

from plexutils.media.movie_list import MovieList
from plexutils.media.movie import Movie


class TestMovieList(unittest.TestCase):
    """test class for the MovieList class"""

    def test_medialist_add(self):
        """tests the add method of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        movie_list.add(Movie("The Matrix Reloaded (2003) {tvdb-553}.mp4"))
        movie_list.add(Movie("The Matrix Revolutions (2003) {tvdb-554}.mp4"))
        self.assertEqual(3, len(movie_list.movies))


if __name__ == '__main__':
    unittest.main()

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

    def test_property_movies(self):
        """tests the movies property of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        self.assertEqual(1, len(movie_list.movies))

    def test_get_movie(self):
        """tests the get_movie method of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        movie_list.add(Movie("The Matrix Reloaded (2003) {tvdb-553}.mp4"))
        movie_list.add(Movie("The Matrix Revolutions (2003) {tvdb-554}.mp4"))
        movie: Movie = movie_list.get_movie(475)
        self.assertTrue(movie.is_valid())
        self.assertEqual("Happy Death Day (2017) {tvdb-475}.mp4", movie.filename)
        self.assertEqual(475, movie.tvdbid)


if __name__ == '__main__':
    unittest.main()

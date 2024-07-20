"""
    This module contains unit tests for the MovieList class.
"""

import unittest
from typing import Optional

from plexutils.media.movie import Movie
from plexutils.media.movie_list import MovieList


class TestMovieList(unittest.TestCase):
    """test class for the MovieList class"""

    def test_medialist_add(self) -> None:
        """tests the add method of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        movie_list.add(Movie("The Matrix Reloaded (2003) {tvdb-553}.mp4"))
        movie_list.add(Movie("The Matrix Revolutions (2003) {tvdb-554}.mp4"))
        self.assertEqual(3, len(movie_list.movies))

    def test_property_movies(self) -> None:
        """tests the movies property of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        self.assertEqual(1, len(movie_list.movies))

    def test_get_movie(self) -> None:
        """tests the get_movie method of the MovieList class"""
        movie_list = MovieList()
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        movie_list.add(Movie("The Matrix Reloaded (2003) {tvdb-553}.mp4"))
        movie_list.add(Movie("The Matrix Revolutions (2003) {tvdb-554}.mp4"))

        movie: Optional[Movie] = movie_list.get_movie(475)
        self.assertIsNotNone(movie)

        if movie is not None:
            self.assertTrue(movie.is_valid())
            self.assertEqual("Happy Death Day (2017) {tvdb-475}.mp4", movie.filename)
            self.assertEqual(475, movie.tvdbid)

    def test_is_empty(self) -> None:
        """tests the is_empty method of the MovieList class"""
        movie_list = MovieList()
        self.assertTrue(movie_list.is_empty())
        movie_list.add(Movie("Happy Death Day (2017) {tvdb-475}.mp4"))
        self.assertFalse(movie_list.is_empty())
        movie_list.add(Movie("The Matrix Reloaded (2003) {tvdb-553}.mp4"))
        self.assertFalse(movie_list.is_empty())


if __name__ == "__main__":
    unittest.main()

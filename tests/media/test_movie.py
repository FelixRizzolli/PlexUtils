"""
    This module contains unit tests for the Movie class.
"""
import unittest

from plexutils.media.movie import Movie


class TestMovie(unittest.TestCase):
    """test class for the Movie class"""

    def test_property_tvdbid(self) -> None:
        """tests the tvdbid property of the Movie class"""
        movie: Movie = Movie("Happy Death Day (2017) {tvdb-475}.mp4")
        self.assertEqual(475, movie.tvdbid)

    def test_property_filename(self) -> None:
        """tests the filename property of the Movie class"""
        movie: Movie = Movie("Happy Death Day (2017) {tvdb-475}.mp4")
        self.assertEqual("Happy Death Day (2017) {tvdb-475}.mp4", movie.filename)

    def test_is_valid(self) -> None:
        """tests the is_valid method of the Movie class"""
        movie: Movie = Movie("Happy Death Day (2017) {tvdb-475}.mp4")
        self.assertTrue(movie.is_valid())

        movie_invalid_tvdbid_1: Movie = Movie("Happy Death Day (2017) {tvdb-x}.mp4")
        self.assertFalse(movie_invalid_tvdbid_1.is_valid())

        movie_invalid_tvdbid_2: Movie = Movie("Happy Death Day (2017).mp4")
        self.assertFalse(movie_invalid_tvdbid_2.is_valid())


if __name__ == '__main__':
    unittest.main()

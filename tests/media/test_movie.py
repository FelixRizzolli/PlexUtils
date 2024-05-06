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


if __name__ == '__main__':
    unittest.main()

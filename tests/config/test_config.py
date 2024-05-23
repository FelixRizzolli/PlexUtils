"""
This module contains unit tests for the Config class in the plexutils.config package.
"""

import unittest
from plexutils.config.config import Config
from plexutils.config.plex_library_infos import PlexLibraryInfos
from plexutils.config.tvdb_credentials import TVDBCredentials


class TestConfig(unittest.TestCase):
    """
    This class contains unit tests for the Config class.
    """

    def setUp(self):
        """
        Set up test data for the unit tests.
        """
        self.movie_library1 = PlexLibraryInfos(
            type="movie",
            name="Movies1",
            path="/path/to/movies1",
            dub_lang="en",
            sub_lang="fr",
        )
        self.movie_library2 = PlexLibraryInfos(
            type="movie",
            name="Movies2",
            path="/path/to/movies2",
            dub_lang="en",
            sub_lang="fr",
        )
        self.tvshow_library1 = PlexLibraryInfos(
            type="tvshow",
            name="TV Shows1",
            path="/path/to/tvshows1",
            dub_lang="en",
            sub_lang="fr",
        )
        self.tvshow_library2 = PlexLibraryInfos(
            type="tvshow",
            name="TV Shows2",
            path="/path/to/tvshows2",
            dub_lang="en",
            sub_lang="fr",
        )
        self.tvdb = TVDBCredentials(
            api_key="test_api_key",
            api_pin="test_user_key"
        )

    def test_multiple_movie_libraries(self):
        """
        Test that the get_movie_libraries method correctly returns all movie libraries.
        """
        config = Config(
            language="en_US",
            libraries=[self.movie_library1, self.movie_library2],
            tvdb=self.tvdb
        )
        movie_libraries = config.get_movie_libraries()

        self.assertEqual(2, len(movie_libraries))
        self.assertEqual(self.movie_library1, movie_libraries[0])
        self.assertEqual(self.movie_library2, movie_libraries[1])

    def test_multiple_tvshow_libraries(self):
        """
        Test that the get_tvshow_libraries method correctly returns all TV show libraries.
        """
        config = Config(
            language="en_US",
            libraries=[self.tvshow_library1, self.tvshow_library2],
            tvdb=self.tvdb
        )
        tvshow_libraries = config.get_tvshow_libraries()

        self.assertEqual(2, len(tvshow_libraries))
        self.assertEqual(tvshow_libraries[0], self.tvshow_library1)
        self.assertEqual(tvshow_libraries[1], self.tvshow_library2)

    def test_config_without_movie_library(self):
        """
        Test that the get_tvshow_libraries method correctly handles the case where there
        are no TV show libraries.
        """
        config = Config(
            language="en_US",
            libraries=[self.tvshow_library1, self.tvshow_library2],
            tvdb=self.tvdb
        )
        movie_libraries = config.get_movie_libraries()

        self.assertEqual(0, len(movie_libraries))

    def test_config_without_tvshow_library(self):
        """
        Test that the get_tvshow_libraries method correctly handles the case where there
        are no TV show libraries.
        """
        config = Config(
            language="en_US",
            libraries=[self.movie_library1, self.movie_library2],
            tvdb=self.tvdb
        )
        tvshow_libraries = config.get_tvshow_libraries()

        self.assertEqual(0, len(tvshow_libraries))


if __name__ == "__main__":
    unittest.main()

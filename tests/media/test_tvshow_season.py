"""
    This module contains unit tests for the TVShowSeason class.
"""
import unittest

from plexutils.media.tvshow_season import TVShowSeason


class TestTVShowSeason(unittest.TestCase):
    """test class for the TVShowSeason class"""

    def test_property_season_id(self) -> None:
        """tests the season_id property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertEqual(1, season.season_id)


if __name__ == '__main__':
    unittest.main()

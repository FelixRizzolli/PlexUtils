"""
    This module contains unit tests for the TVShowSeason class.
"""
import unittest

from plexutils.media.tvshow_season import TVShowSeason
from plexutils.media.tvshow_episode import TVShowEpisode


class TestTVShowSeason(unittest.TestCase):
    """test class for the TVShowSeason class"""

    def test_property_season_id(self) -> None:
        """tests the season_id property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertEqual(1, season.season_id)

    def test_property_dirname(self) -> None:
        """tests the dirname property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertEqual("season 01", season.dirname)


if __name__ == '__main__':
    unittest.main()

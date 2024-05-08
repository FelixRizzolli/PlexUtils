"""
    This module contains unit tests for the TVShow class.
"""
import unittest

from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason


class TestTVShow(unittest.TestCase):
    """test class for the TVShow class"""

    def test_property_tvdbid(self) -> None:
        """tests the tvdbid property of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertEqual(79525, tvshow.tvdbid)

    def test_property_dirname(self) -> None:
        """tests the dirname property of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertEqual('Code Geass (2006) {tvdb-79525}', tvshow.dirname)

    def test_property_season(self) -> None:
        """tests the season property of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertEqual(0, len(tvshow.seasons))
        tvshow.add_season(TVShowSeason('season 01'))
        self.assertEqual(1, len(tvshow.seasons))
        tvshow.add_season(TVShowSeason('season 02'))
        self.assertEqual(2, len(tvshow.seasons))


if __name__ == '__main__':
    unittest.main()

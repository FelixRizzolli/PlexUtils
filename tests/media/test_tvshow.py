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

    def test_property_seasonids(self) -> None:
        """tests the seasonids property of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        tvshow.add_season(TVShowSeason('season 01'))
        tvshow.add_season(TVShowSeason('season 02'))
        self.assertEqual([1, 2], tvshow.seasonids)

    def test_is_valid(self) -> None:
        """tests the is_valid method of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertTrue(tvshow.is_valid())

        tvshow_invalid_tvdbid_1: TVShow = TVShow('Code Geass (2006) {tvdb-x}')
        self.assertFalse(tvshow_invalid_tvdbid_1.is_valid())

        tvshow_invalid_tvdbid_2: TVShow = TVShow('Code Geass (2006)')
        self.assertFalse(tvshow_invalid_tvdbid_2.is_valid())

    def test_add_season(self) -> None:
        """tests the add_season method of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        tvshow.add_season(TVShowSeason('season 01'))
        self.assertEqual(1, len(tvshow.seasons))
        tvshow.add_season(TVShowSeason('season 02'))
        self.assertEqual(2, len(tvshow.seasons))

    def test_get_season(self) -> None:
        """tests the get_season method of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        tvshow.add_season(TVShowSeason('season 01'))
        tvshow.add_season(TVShowSeason('season 02'))

        season_01: TVShowSeason = tvshow.get_season(1)
        self.assertTrue(season_01.is_valid())
        self.assertEqual('season 01', season_01.dirname)

        season_02: TVShowSeason = tvshow.get_season(2)
        self.assertTrue(season_02.is_valid())
        self.assertEqual('season 02', season_02.dirname)

    def test_is_empty(self) -> None:
        """tests the is_empty method of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertTrue(tvshow.is_empty())
        tvshow.add_season(TVShowSeason('season 01'))
        self.assertFalse(tvshow.is_empty())
        tvshow.add_season(TVShowSeason('season 02'))
        self.assertFalse(tvshow.is_empty())


if __name__ == '__main__':
    unittest.main()

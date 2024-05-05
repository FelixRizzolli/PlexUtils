"""
    This module contains unit tests for the media modules.
"""
import unittest

from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.media.tvshow_episode import TVShowEpisode


class TestTVShowList(unittest.TestCase):
    """test class for the TVShowList class"""

    def test_tvshowlist_is_empty(self):
        """tests the is_empty method of the TVShowList class"""
        tvshowlist = TVShowList()
        self.assertTrue(tvshowlist.is_empty())
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        self.assertFalse(tvshowlist.is_empty())
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))
        self.assertFalse(tvshowlist.is_empty())

    def test_tvshowlist_add_tvshow(self):
        """tests the add_tvshow method of the TVShowList class"""
        tvshowlist = TVShowList()
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        self.assertEqual(1, len(tvshowlist.get_tvshows()))
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))
        self.assertEqual(2, len(tvshowlist.get_tvshows()))

    def test_tvshowlist_get_tvshow(self):
        """tests the get_tvshow method of the TVShowList class"""
        tvshowlist = TVShowList()
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))

        codegeass = tvshowlist.get_tvshow(79525)
        self.assertTrue(codegeass.is_valid())
        self.assertEqual("Code Geass (2006) {tvdb-79525}", codegeass.get_dirname())

        got = tvshowlist.get_tvshow(121361)
        self.assertTrue(got.is_valid())
        self.assertEqual("Game of Thrones (2011) {tvdb-121361}", got.get_dirname())

    def test_tvshow_get_tvdbid(self):
        """tests the get_tvdbid method of the TVShow class"""
        tvshow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertEqual(79525, tvshow.get_tvdbid())

    def test_tvshowepisode_get_id(self):
        """tests the get_id method of the TVShowEpisode class"""
        episode = TVShowEpisode("Code Geass (2006) - s01e01 - The Day a New Demon Was Born")
        self.assertEqual(1, episode.get_id())

    def test_tvshowseason_get_id(self):
        """tests the get_id method of the TVShowSeason class"""
        season = TVShowSeason("season 01")
        self.assertEqual(1, season.get_id())


if __name__ == '__main__':
    unittest.main()

"""
    This module contains unit tests for the TVShowList class.
"""
import unittest

from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow import TVShow


class TestTVShowList(unittest.TestCase):
    """test class for the TVShowList class"""

    def test_is_empty(self) -> None:
        """tests the is_empty method of the TVShowList class"""
        tvshowlist: TVShowList = TVShowList()
        self.assertTrue(tvshowlist.is_empty())
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        self.assertFalse(tvshowlist.is_empty())
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))
        self.assertFalse(tvshowlist.is_empty())

    def test_add_tvshow(self) -> None:
        """tests the add_tvshow method of the TVShowList class"""
        tvshowlist: TVShowList = TVShowList()
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        self.assertEqual(1, len(tvshowlist.get_tvshows()))
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))
        self.assertEqual(2, len(tvshowlist.get_tvshows()))

    def test_get_tvshow(self) -> None:
        """tests the get_tvshow method of the TVShowList class"""
        tvshowlist: TVShowList = TVShowList()
        tvshowlist.add_tvshow(TVShow("Code Geass (2006) {tvdb-79525}"))
        tvshowlist.add_tvshow(TVShow("Game of Thrones (2011) {tvdb-121361}"))

        codegeass: TVShow = tvshowlist.get_tvshow(79525)
        self.assertTrue(codegeass.is_valid())
        self.assertEqual("Code Geass (2006) {tvdb-79525}", codegeass.get_dirname())

        got: TVShow = tvshowlist.get_tvshow(121361)
        self.assertTrue(got.is_valid())
        self.assertEqual("Game of Thrones (2011) {tvdb-121361}", got.get_dirname())


if __name__ == '__main__':
    unittest.main()
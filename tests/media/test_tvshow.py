"""
    This module contains unit tests for the TVShow class.
"""
import unittest

from plexutils.media.tvshow import TVShow


class TestTVShow(unittest.TestCase):
    """test class for the TVShow class"""

    def test_get_tvdbid(self) -> None:
        """tests the get_tvdbid method of the TVShow class"""
        tvshow: TVShow = TVShow('Code Geass (2006) {tvdb-79525}')
        self.assertEqual(79525, tvshow.tvdbid)


if __name__ == '__main__':
    unittest.main()

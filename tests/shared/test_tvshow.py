import unittest

from tvshow import TVShow


class TestTVShow(unittest.TestCase):
    def test_something(self):
        tvshow = TVShow('Code Geass (2006) {tvdb-79525}')

        self.assertEqual(79525, tvshow.get_tvdbid())



if __name__ == '__main__':
    unittest.main()

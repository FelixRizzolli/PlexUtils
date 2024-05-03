import unittest

from tvshow_season import TVShowSeason


class TestTVShowSeason(unittest.TestCase):
    def test_something(self):
        season = TVShowSeason(79525, "season 01")

        self.assertEqual(1, season.get_id())


if __name__ == '__main__':
    unittest.main()

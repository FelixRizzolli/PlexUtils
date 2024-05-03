import unittest

from tvshow_episode import TVShowEpisode

class TestTVShowEpisode(unittest.TestCase):
    def test_something(self):
        episode = TVShowEpisode(79525, 1, "Code Geass (2006) - s01e01 - The Day a New Demon Was Born")

        self.assertEqual(1, episode.get_id())


if __name__ == '__main__':
    unittest.main()

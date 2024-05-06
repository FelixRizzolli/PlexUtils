"""
    This module contains unit tests for the TVShowEpisode class.
"""
import unittest

from plexutils.media.tvshow_episode import TVShowEpisode


class TestTVShowEpisode(unittest.TestCase):
    """test class for the TVShowEpisode class"""

    def test_tvshowepisode_get_id(self) -> None:
        """tests the get_id method of the TVShowEpisode class"""
        episode: TVShowEpisode = TVShowEpisode(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born"
        )
        self.assertEqual(1, episode.episode_id)


if __name__ == '__main__':
    unittest.main()

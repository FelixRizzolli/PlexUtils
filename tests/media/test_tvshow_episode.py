"""
    This module contains unit tests for the TVShowEpisode class.
"""
import unittest

from plexutils.media.tvshow_episode import TVShowEpisode


class TestTVShowEpisode(unittest.TestCase):
    """test class for the TVShowEpisode class"""

    def test_property_episode_id(self) -> None:
        """tests the episode_id property of the TVShowEpisode class"""
        episode: TVShowEpisode = TVShowEpisode(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born.mp4"
        )
        self.assertEqual(1, episode.episode_id)

    def test_property_filename(self) -> None:
        """tests the filename property of the TVShowEpisode class"""
        episode: TVShowEpisode = TVShowEpisode(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born.mp4"
        )
        self.assertEqual(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born.mp4",
            episode.filename
        )



if __name__ == '__main__':
    unittest.main()

"""
    This module contains unit tests for the TVShowSeason class.
"""
import unittest

from plexutils.media.tvshow_season import TVShowSeason
from plexutils.media.tvshow_episode import TVShowEpisode


class TestTVShowSeason(unittest.TestCase):
    """test class for the TVShowSeason class"""

    def test_property_season_id(self) -> None:
        """tests the season_id property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertEqual(1, season.season_id)

    def test_property_dirname(self) -> None:
        """tests the dirname property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertEqual("season 01", season.dirname)

    def test_property_episodes(self) -> None:
        """tests the episodes property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born.mp4"
        ))
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e02 - The White Knight Awakens.mp4"
        ))
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e03 - The False Classmate.mp4"
        ))
        self.assertEqual(3, len(season.episodes))

    def test_property_episodeids(self) -> None:
        """tests the episodeids property of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e01 - The Day a New Demon Was Born.mp4"
        ))
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e02 - The White Knight Awakens.mp4"
        ))
        season.add_episode(TVShowEpisode(
            "Code Geass (2006) - s01e03 - The False Classmate.mp4"
        ))
        self.assertEqual([1, 2, 3], season.episodeids)

    def test_is_valid(self) -> None:
        """tests the is_valid method of the TVShowSeason class"""
        season: TVShowSeason = TVShowSeason("season 01")
        self.assertTrue(season.is_valid())

        season_invalid_seasonid: TVShowSeason = TVShowSeason("season 0x1")
        self.assertFalse(season_invalid_seasonid.is_valid())


if __name__ == '__main__':
    unittest.main()

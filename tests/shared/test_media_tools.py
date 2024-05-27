"""
This module contains unit tests for the functions in the media_tools.py module.
"""

import unittest
from typing import Optional

from plexutils.shared.media_tools import (
    extract_episodeid,
    extract_seasonid,
    extract_seasonid_from_episode,
    extract_tvdbid,
)


class TestMediaTools(unittest.TestCase):
    """
    This class contains unit tests for the functions in the media_tools.py module.
    """

    def test_extract_tvdbid(self) -> None:
        """
        Test case for the `extract_tvdbid` function. It tests the function with
        different directory names.
        """
        got: Optional[int] = extract_tvdbid("Game of Thrones (2011) {tvdb-121361}")
        self.assertEqual(121361, got)

        you_zitsu: Optional[int] = extract_tvdbid("Classroom of the Elite (2017)")
        self.assertIsNone(you_zitsu)

        matrix: Optional[int] = extract_tvdbid("The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(169, matrix)

        baby_driver: Optional[int] = extract_tvdbid("Baby Driver (2017).mp4")
        self.assertIsNone(baby_driver)

    def test_extract_seasonid(self) -> None:
        """
        Test case for the `extract_seasonid` function. It tests the function with
        different directory names.
        """
        season_1: Optional[int] = extract_seasonid("Season 01")
        self.assertEqual(1, season_1)

        season_2: Optional[int] = extract_seasonid("Season 02")
        self.assertEqual(2, season_2)

        season_a: Optional[int] = extract_seasonid("Season a")
        self.assertIsNone(season_a)

    def test_extract_episodeid(self) -> None:
        """
        Test case for the `extract_episodeid` function. It tests the function with
        different file names.
        """
        ep_1: Optional[int] = extract_episodeid(
            "Game of Thrones (2011) - s01e01 - Winter Is Coming.mp4"
        )
        self.assertEqual(1, ep_1)

        ep_25: Optional[int] = extract_episodeid(
            "Code Geass (2006) - s01e25 - Zero.mp4"
        )
        self.assertEqual(25, ep_25)

        ep_x3: Optional[int] = extract_episodeid(
            "Code Geass (2006) - s01ex3 - Zero.mp4"
        )
        self.assertIsNone(ep_x3)

    def test_extract_seasonid_from_episode(self) -> None:
        """
        Test case for the `extract_seasonid_from_episode` function. It tests the function
        with different file names.
        """
        season_1: Optional[int] = extract_seasonid_from_episode(
            "Game of Thrones (2011) - s01e01 - Winter Is Coming.mp4"
        )
        self.assertEqual(1, season_1)

        season_2: Optional[int] = extract_seasonid_from_episode(
            "Code Geass (2006) - s02e13 - Assassin from the Past.mp4"
        )
        self.assertEqual(2, season_2)

        season_x1: Optional[int] = extract_seasonid_from_episode(
            "Code Geass (2006) - sx1e13 - Assassin from the Past.mp4"
        )
        self.assertIsNone(season_x1)


if __name__ == "__main__":
    unittest.main()

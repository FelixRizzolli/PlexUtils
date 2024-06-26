"""
    This module contains unit tests for the functions in utils.py.
"""

import unittest
from typing import Optional

from plexutils.shared.utils import (
    extract_episodeid,
    extract_seasonid,
    extract_seasonid_from_episode,
    extract_tvdbid,
    is_future_date,
    is_past_date,
)


class TestUtils(unittest.TestCase):
    """test class for the functions in utils.py"""

    def test_extract_tvdbid(self) -> None:
        """tests the extract_tvdbid function"""
        got: Optional[int] = extract_tvdbid("Game of Thrones (2011) {tvdb-121361}")
        self.assertEqual(121361, got)

        you_zitsu: Optional[int] = extract_tvdbid("Classroom of the Elite (2017)")
        self.assertIsNone(you_zitsu)

        matrix: Optional[int] = extract_tvdbid("The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(169, matrix)

        baby_driver: Optional[int] = extract_tvdbid("Baby Driver (2017).mp4")
        self.assertIsNone(baby_driver)

    def test_extract_seasonid(self) -> None:
        """tests the extract_seasonid function"""
        season_1: Optional[int] = extract_seasonid("Season 01")
        self.assertEqual(1, season_1)

        season_2: Optional[int] = extract_seasonid("Season 02")
        self.assertEqual(2, season_2)

        season_a: Optional[int] = extract_seasonid("season a")
        self.assertIsNone(season_a)

    def test_extract_episodeid(self) -> None:
        """tests the extract_episodeid function"""
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
        """tests the extract_seasonid_from_episode function"""
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

    def test_is_past_date(self) -> None:
        """tests the is_past_date function"""
        date_to_check: str = "2000-01-01"
        self.assertTrue(is_past_date(date_to_check))
        date_to_check: str = "3000-01-01"
        self.assertFalse(is_past_date(date_to_check))

    def test_is_future_date(self) -> None:
        """tests the is_future_date function"""
        date_to_check: str = "2000-01-01"
        self.assertFalse(is_future_date(date_to_check))
        date_to_check: str = "3000-01-01"
        self.assertTrue(is_future_date(date_to_check))


if __name__ == "__main__":
    unittest.main()

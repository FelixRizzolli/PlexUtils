import unittest

from utils import extract_tvdbid, extract_seasonid, extract_episodeid, extract_seasonid_from_episode

class TestUtils(unittest.TestCase):
    def test_extract_tvdbid(self):
        got = extract_tvdbid("Game of Thrones (2011) {tvdb-121361}")
        self.assertEqual(121361, got)

        you_zitsu = extract_tvdbid("Classroom of the Elite (2017)")
        self.assertIsNone(you_zitsu)

        matrix = extract_tvdbid("The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(169, matrix)

        baby_driver = extract_tvdbid("Baby Driver (2017).mp4")
        self.assertIsNone(baby_driver)

    def test_extract_seasonid(self):
        season1 = extract_seasonid("season 01")
        self.assertEqual(1, season1)

        season2 = extract_seasonid("season 02")
        self.assertEqual(2, season2)

        season3 = extract_seasonid("season a")
        self.assertIsNone(season3)

    def test_extract_episodeid(self):
        ep1 = extract_episodeid("Game of Thrones (2011) - s01e01 - Winter Is Coming.mp4")
        self.assertEqual(1, ep1)

        ep25 = extract_episodeid("Code Geass (2006) - s01e25 - Zero.mp4")
        self.assertEqual(25, ep25)

        epx3 = extract_episodeid("Code Geass (2006) - s01ex3 - Zero.mp4")
        self.assertIsNone(epx3)

    def test_extract_seasonid_from_episode(self):
        pass


if __name__ == '__main__':
    unittest.main()

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
        pass

    def test_extract_episodeid(self):
        pass

    def test_extract_seasonid_from_episode(self):
        pass


if __name__ == '__main__':
    unittest.main()

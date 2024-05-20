"""
    This module contains unit tests for the TestPlexTvshowsCrawler class.
"""

import json
import os
import unittest
from typing import Optional

from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_episode import TVShowEpisode
from plexutils.media.tvshow_list import TVShowList
from plexutils.media.tvshow_season import TVShowSeason


class TestPlexTVShowCrawler(unittest.TestCase):
    """test class for the PlexTvshowsCrawler class"""

    crawler: PlexTVShowCrawler
    tvshow_directories: dict

    @classmethod
    def setUpClass(cls) -> None:
        # Define directory paths
        current_script_dir: str = os.path.dirname(os.path.realpath(__file__))
        data_dir: str = os.path.join(current_script_dir, "../../data")
        scripts_data_dir: str = os.path.join(current_script_dir, "../../scripts/data")
        tvshows_dir: str = os.path.join(data_dir, "tvshows", "animes")

        # Open the JSON file
        tvshows_data_file: str = os.path.join(
            scripts_data_dir, "tvshows", "anime_tvshow_files.json"
        )
        with open(tvshows_data_file, "r", encoding="utf-8") as f:
            # Load the JSON data into 0.-a Python dictionary
            cls.tvshow_directories = json.load(f)["tvshow_files"]

        # initialize crawler
        cls.crawler = PlexTVShowCrawler(tvshows_dir)
        cls.crawler.crawl()

    def test_crawl_get_tvshows_count(self) -> None:
        """
        tests the get_tvshows method
            by counting the number of tvshows
            and comparing the result with the expected number of tvshows
        """
        tvshowlist = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            tvshows: list[TVShow] = tvshowlist.tvshows
            invalid_tvshows: list[str] = self.crawler.get_invalid_tvshows()
            self.assertEqual(
                len(self.tvshow_directories), len(tvshows) + len(invalid_tvshows)
            )

    def test_crawl_get_tvshows_object(self) -> None:
        """
        tests the get_tvshows method
            by selecting a specific tvshow
            and comparing the result with the expected data
        """
        tvshowlist: Optional[TVShowList] = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            codegeass: Optional[TVShow] = tvshowlist.get_tvshow(79525)
            if codegeass is not None:
                self.assertEqual(codegeass.dirname, "Code Geass (2006) {tvdb-79525}")
                self.assertEqual(codegeass.tvdbid, 79525)

    def test_crawl_get_invalid_tvshows(self) -> None:
        """
        tests the get_invalid_tvshows method
            by selecting the first element in the collection
            and comparing the result with the expected data
        """
        invalid_tvshows: list[str] = self.crawler.get_invalid_tvshows()
        self.assertIn("Classroom of the Elite (2017)", invalid_tvshows)

    def test_crawl_get_seasons_count(self) -> None:
        """
        tests the get_seasons method
            by counting the number of seasons
                of a specific tvshow
            and comparing the result with the expected number of seasons
        """
        tvshowlist = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            plex_codegeass: Optional[TVShow] = tvshowlist.get_tvshow(79525)
            if plex_codegeass is not None:
                seasons: list[TVShowSeason] = plex_codegeass.seasons
                test_codegeass: dict = list(
                    filter(
                        lambda tvshow: tvshow["dirname"]
                        == "Code Geass (2006) {tvdb-79525}",
                        self.tvshow_directories,
                    )
                )[0]
                self.assertEqual(len(test_codegeass["seasons"]), len(seasons))

    def test_crawl_get_episodes_count(self) -> None:
        """
        tests the get_episodes method
            by counting the number of episodes
                of a specific season
                of a specific tvshow
            and comparing the result with the expected number of seasons
        """
        tvshowlist = self.crawler.get_tvshowlist()
        if tvshowlist is not None:
            plex_codegeass: Optional[TVShow] = tvshowlist.get_tvshow(79525)
            if plex_codegeass is not None:
                plex_codegeass_s1: Optional[TVShowSeason] = plex_codegeass.get_season(1)
                if plex_codegeass_s1 is not None:
                    episodes: list[TVShowEpisode] = plex_codegeass_s1.episodes
                    test_codegeass: dict = list(
                        filter(
                            lambda tvshow: tvshow["dirname"]
                            == "Code Geass (2006) {tvdb-79525}",
                            self.tvshow_directories,
                        )
                    )[0]
                    test_codegeass_s1: dict = list(
                        filter(
                            lambda season: season["dirname"] == "season 01",
                            test_codegeass["seasons"],
                        )
                    )[0]
                    self.assertEqual(len(test_codegeass_s1["episodes"]), len(episodes))


if __name__ == "__main__":
    unittest.main()

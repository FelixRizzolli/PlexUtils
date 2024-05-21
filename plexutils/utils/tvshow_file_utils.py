"""
    This module contains TvshowFileUtils class.
"""

from typing import Callable

from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.shared.menu import Menu
from plexutils.shared.menu_tools import library_menu_wrapper, print_menu


class TvshowFileUtils:
    """represents the menu and tools for tv show files"""

    def __init__(self, config: dict, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: dict = config

        self.menu_list: Menu = Menu(
            [
                {
                    "id": "1",
                    "name": self.gettext("validate tvshow directory syntax"),
                    "action": lambda: library_menu_wrapper(
                        self.gettext, self.config, "tvshow", self.validate_tvshow_syntax
                    ),
                },
                {
                    "id": "2",
                    "name": self.gettext("validate season directory syntax"),
                    "action": lambda: library_menu_wrapper(
                        self.gettext, self.config, "tvshow", self.validate_season_syntax
                    ),
                },
                {
                    "id": "3",
                    "name": self.gettext("validate episode filename syntax"),
                    "action": lambda: library_menu_wrapper(
                        self.gettext,
                        self.config,
                        "tvshow",
                        self.validate_episode_syntax,
                    ),
                },
            ]
        )

    def get_utils_name(self) -> str:
        """returns the utils name"""
        return self.gettext(
            "TvshowFileUtils - Tools for tvshow directories and episode files"
        )

    def print_menu(self) -> None:
        """prints the menu"""
        print_menu(self.gettext("TvshowFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_tvshow_syntax(self, library_path: str) -> None:
        """
        validates the directory name
            of the tv shows
            from the initialized directory
        """

        crawler: PlexTVShowCrawler = PlexTVShowCrawler(library_path)
        crawler.crawl()

        invalid_tvshows: list[str] = crawler.get_invalid_tvshows()

        if len(invalid_tvshows) == 0:
            self.gettext("No invalid tvshows found")
            input()
            return

        for tvshow in invalid_tvshows:
            print(self.gettext("Invalid tvshow directory: ") + tvshow)

        input()

    def validate_season_syntax(self, library_path: str) -> None:
        """
        validates the directory name
            of the seasons
            of the tv shows
            from the initialized directory
        """

        crawler: PlexTVShowCrawler = PlexTVShowCrawler(library_path)
        crawler.crawl()

        invalid_seasons: list[str] = crawler.get_invalid_seasons()

        if len(invalid_seasons) == 0:
            self.gettext("No invalid seasons found")
            input()
            return

        for season in invalid_seasons:
            print(self.gettext("Invalid season directory: ") + season)

        input()

    def validate_episode_syntax(self, library_path) -> None:
        """
        validates the directory name
            of the episodes
            of the seasons
            of the tv shows
            from the initialized directory
        """

        crawler: PlexTVShowCrawler = PlexTVShowCrawler(library_path)
        crawler.crawl()

        invalid_episodes: list[str] = crawler.get_invalid_episodes()

        if len(invalid_episodes) == 0:
            self.gettext("No invalid episodes found")
            input()
            return

        for episode in invalid_episodes:
            print(self.gettext("Invalid episode filename: ") + episode)

        input()

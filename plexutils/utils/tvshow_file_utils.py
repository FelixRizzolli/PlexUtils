"""
    This module contains TvshowFileUtils class.
"""

from typing import Optional

from plexutils.console.menu import ConsoleMenu
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.shared.menu_tools import library_menu_wrapper


class TvshowFileUtils(ConsoleMenu):
    """represents the menu and tools for tv show files"""

    def __init__(self):
        super().__init__()
        self.title = self.gettext("TvshowFileUtils Menu:")
        self.setup_menu()

    def setup_menu(self) -> None:
        """
        sets up the menu items

        :return: None
        """
        self.add_item(
            {
                "id": "1",
                "name": self.gettext("validate tvshow directory syntax"),
                "action": lambda: library_menu_wrapper(
                    self.gettext, self.config, "tvshow", self.validate_tvshow_syntax
                ),
            }
        )
        self.add_item(
            {
                "id": "2",
                "name": self.gettext("validate season directory syntax"),
                "action": lambda: library_menu_wrapper(
                    self.gettext, self.config, "tvshow", self.validate_season_syntax
                ),
            },
        )
        self.add_item(
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
        )

    def get_utils_name(self) -> str:
        """
        returns the utils name

        :return: The utils name.
        :rtype: str
        """
        return self.gettext(
            "TvshowFileUtils - Tools for tvshow directories and episode files"
        )

    def validate_tvshow_syntax(self, library_path: str) -> None:
        """
        validates the directory name
            of the tv shows
            from the initialized directory

        :param library_path: The path of the library.
        :type library_path: str

        :return: None
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

        :param library_path: The path of the library.
        :type library_path: str

        :return: None
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

    def validate_episode_syntax(self, library_path: str) -> None:
        """
        validates the directory name
            of the episodes
            of the seasons
            of the tv shows
            from the initialized directory

        :param library_path: The path of the library.
        :type library_path: str

        :return: None
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

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a warning message if needed.

        :return: The warning message.
        :rtype: Optional[str]
        """

        if self.config is None:
            return self.gettext("No config found")
        if len(self.config.get_tvshow_libraries()) == 0:
            return self.gettext("No tvshow libraries found")

        return None

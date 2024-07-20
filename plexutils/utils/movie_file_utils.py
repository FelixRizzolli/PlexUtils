"""
    This module contains MovieFileUtils class.
"""

from typing import Optional

from plexutils.console.menu import ConsoleMenu
from plexutils.crawler.plex_movie_crawler import PlexMovieCrawler
from plexutils.shared.menu_tools import library_menu_wrapper


class MovieFileUtils(ConsoleMenu):
    """represents the menu and tools for movie files"""

    def __init__(self):
        super().__init__()
        self.title = self.gettext("MovieFileUtils Menu:")
        self.setup_menu()

    def setup_menu(self) -> None:
        """
        sets up the menu items

        :return: None
        """
        self.add_item(
            {
                "id": "1",
                "name": self.gettext("validate movie filename syntax"),
                "action": lambda: library_menu_wrapper(
                    self.gettext, self.config, "movie", self.validate_movie_syntax
                ),
            }
        )

    def get_utils_name(self) -> str:
        """
        returns the utils name

        :return: the utils name
        :rtype: str
        """
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def validate_movie_syntax(self, library_path: str) -> None:
        """
        validates the filenames
            of the movies
            from the initialized directory

        :param library_path: the path to the library
        :type library_path: str

        :return: None
        """

        crawler: PlexMovieCrawler = PlexMovieCrawler(library_path)
        crawler.crawl()

        invalid_movies: list[str] = crawler.get_invalid_movies()

        if len(invalid_movies) == 0:
            self.gettext("No invalid movie files found")
            input()
            return

        for movie in invalid_movies:
            print(self.gettext("Invalid movie file: ") + movie)

        input()

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a warning message if needed.

        :return: The warning message.
        :rtype: str
        """

        if self.config is None:
            return self.gettext("No config found")
        if len(self.config.get_movie_libraries()) == 0:
            return self.gettext("No movie libraries found")

        return None

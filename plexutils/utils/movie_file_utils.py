"""
    This module contains MovieFileUtils class.
"""

from typing import Callable

from plexutils.crawler.plex_movie_crawler import PlexMovieCrawler
from plexutils.shared.menu import Menu
from plexutils.shared.menu_tools import library_menu_wrapper, print_menu


class MovieFileUtils:
    """represents the menu and tools for movie files"""

    def __init__(self, config: dict, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: dict = config

        self.menu_list: Menu = Menu(
            [
                {
                    "id": "1",
                    "name": self.gettext("validate movie filename syntax"),
                    "action": lambda: library_menu_wrapper(
                        self.gettext, self.config, "movie", self.validate_movie_syntax
                    ),
                },
            ]
        )

    def get_utils_name(self) -> str:
        """returns the utils name"""
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self) -> None:
        """prints the menu"""
        print_menu(self.gettext("MovieFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_movie_syntax(self, library_path: str) -> None:
        """
        validates the filenames
            of the movies
            from the initialized directory
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

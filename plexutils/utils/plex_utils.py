"""
    This module contains PlexUtils class.
"""

from typing import Callable

from plexutils.shared.menu import Menu
from plexutils.shared.utils import print_menu
from plexutils.utils.movie_file_utils import MovieFileUtils
from plexutils.utils.tvdb_utils import TVDBUtils
from plexutils.utils.tvshow_file_utils import TvshowFileUtils


# pylint: disable=too-few-public-methods
class PlexUtils:
    """represents the menu and tools for plex"""

    def __init__(self, config: dict, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: dict = config

        self.movie_file_utils: MovieFileUtils = MovieFileUtils(config, gettext)
        self.tvshow_file_utils: TvshowFileUtils = TvshowFileUtils(config, gettext)
        self.tvdb_utils: TVDBUtils = TVDBUtils(config, gettext)

        self.menu_list: Menu = Menu(
            [
                {
                    "id": "1",
                    "name": self.movie_file_utils.get_utils_name(),
                    "action": self.movie_file_utils.print_menu,
                },
                {
                    "id": "2",
                    "name": self.tvshow_file_utils.get_utils_name(),
                    "action": self.tvshow_file_utils.print_menu,
                },
                {
                    "id": "3",
                    "name": self.tvdb_utils.get_utils_name(),
                    "action": self.tvdb_utils.print_menu,
                },
            ]
        )

    def print_menu(self) -> None:
        """prints the menu"""
        print_menu(self.gettext("PlexUtils Menu:"), self.gettext, self.menu_list)

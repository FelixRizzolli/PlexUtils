"""
    This module contains PlexUtils class.
"""

from typing import Callable

from plexutils.config.config import Config
from plexutils.shared.console_menu import ConsoleMenu
from plexutils.shared.menu_tools import print_menu
from plexutils.utils.movie_file_utils import MovieFileUtils
from plexutils.utils.tvdb_utils import TVDBUtils
from plexutils.utils.tvshow_file_utils import TvshowFileUtils


# pylint: disable=too-few-public-methods
class PlexUtils:
    """represents the menu and tools for plex"""

    def __init__(self, config: Config, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: Config = config

        self.movie_file_utils: MovieFileUtils = MovieFileUtils(config, gettext)
        self.tvshow_file_utils: TvshowFileUtils = TvshowFileUtils(config, gettext)
        self.tvdb_utils: TVDBUtils = TVDBUtils(config, gettext)

        self.menu_list: ConsoleMenu = ConsoleMenu(
            menu_list=[
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
            ],
            is_main_menu=True,
        )

    def print_menu(self) -> None:
        """prints the menu"""
        print_menu(
            self.gettext("PlexUtils Menu:"), self.gettext, self.menu_list, self.config
        )

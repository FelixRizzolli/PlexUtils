"""
    This module contains PlexUtils class.
"""

from typing import Optional

from plexutils.console.menu import ConsoleMenu
from plexutils.console.settings_menu import SettingsConsoleMenu
from plexutils.utils.movie_file_utils import MovieFileUtils
from plexutils.utils.tvdb_utils import TVDBUtils
from plexutils.utils.tvshow_file_utils import TvshowFileUtils


# pylint: disable=too-few-public-methods
class PlexUtils(ConsoleMenu):
    """represents the menu and tools for plex"""

    def __init__(self):
        self.movie_file_utils: MovieFileUtils = MovieFileUtils()
        self.tvshow_file_utils: TvshowFileUtils = TvshowFileUtils()
        self.tvdb_utils: TVDBUtils = TVDBUtils()
        self.settings_menu: SettingsConsoleMenu = SettingsConsoleMenu()

        super().__init__(is_main_menu=True)
        self.title = self.gettext("PlexUtils Menu:")
        self.setup_menu()

    def setup_menu(self) -> None:
        """
        sets up the menu items

        :return: None
        """
        self.add_item(
            {
                "id": "1",
                "name": self.movie_file_utils.get_utils_name(),
                "action": self.movie_file_utils.print_menu,
            }
        )
        self.add_item(
            {
                "id": "2",
                "name": self.tvshow_file_utils.get_utils_name(),
                "action": self.tvshow_file_utils.print_menu,
            },
        )
        self.add_item(
            {
                "id": "3",
                "name": self.tvdb_utils.get_utils_name(),
                "action": self.tvdb_utils.print_menu,
            },
        )
        self.add_item(
            {
                "id": "S",
                "name": self.settings_menu.get_utils_name(),
                "action": self.settings_menu.print_menu,
            },
        )

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a warning message if needed.

        :return: The warning message.
        :rtype: Optional[str]
        """
        return None

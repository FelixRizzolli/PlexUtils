"""
This module contains the SettingsConsoleMenu class which is used to create and manage the settings
menu in the console.
"""

from plexutils.console.menu import ConsoleMenu


class SettingsConsoleMenu(ConsoleMenu):
    """
    A class used to represent the settings menu in the console.
    """

    def __init__(self):
        super().__init__(
            title=self.gettext("Settings Menu"),
            menu_list=[
                {
                    "id": "1",
                    "name": self.gettext("Change Language"),
                    "function": self.change_language,
                },
                {
                    "id": "2",
                    "name": self.gettext("Change TVDB Credentials"),
                    "function": self.change_tvdb_credentials,
                },
                {
                    "id": "3",
                    "name": self.gettext("Add a Plex Library"),
                    "function": self.change_plex_libraries,
                },
                {
                    "id": "4",
                    "name": self.gettext("Remove a Plex Library"),
                    "function": self.change_plex_libraries,
                },
            ],
            is_main_menu=False,
        )

    def get_utils_name(self) -> str:
        """returns the utils name"""
        return self.gettext("Settings")

    def change_language(self) -> None:
        """
        Changes the language of the application.
        """
        print("change_language()")

    def change_tvdb_credentials(self) -> None:
        """
        Changes the TVDB credentials of the application.
        """
        print("change_tvdb_credentials()")

    def change_plex_libraries(self) -> None:
        """
        Changes the Plex libraries of the application.
        """
        print("change_plex_libraries()")

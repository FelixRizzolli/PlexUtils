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
        super().__init__()
        self.title = self.gettext("Settings Menu:")
        self.setup_menu()

    def setup_menu(self):
        """sets up the menu items"""
        self.add_item(
            {
                "id": "1",
                "name": self.gettext("Change Language"),
                "action": self.change_language,
            }
        )
        self.add_item(
            {
                "id": "2",
                "name": self.gettext("Change TVDB Credentials"),
                "action": self.change_tvdb_credentials,
            }
        )
        self.add_item(
            {
                "id": "3",
                "name": self.gettext("Add a Plex Library"),
                "action": self.change_plex_libraries,
            }
        )
        self.add_item(
            {
                "id": "4",
                "name": self.gettext("Remove a Plex Library"),
                "action": self.change_plex_libraries,
            }
        )

    def get_utils_name(self) -> str:
        """returns the utils name"""
        return self.gettext("Settings")

    def change_language(self) -> None:
        """
        Changes the language of the application.
        """
        print("change_language()")
        input(self.gettext("Press Enter to continue..."))

    def change_tvdb_credentials(self) -> None:
        """
        Changes the TVDB credentials of the application.
        """
        print("change_tvdb_credentials()")
        input(self.gettext("Press Enter to continue..."))

    def change_plex_libraries(self) -> None:
        """
        Changes the Plex libraries of the application.
        """
        print("change_plex_libraries()")
        input(self.gettext("Press Enter to continue..."))

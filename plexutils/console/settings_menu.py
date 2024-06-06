"""
This module contains the SettingsConsoleMenu class which is used to create and manage the settings
menu in the console.
"""

import os

from plexutils.console.menu import ConsoleMenu, clear_console
from plexutils.shared.config_tools import save_config_to_file


def get_config_path() -> str:
    """returns the path to the config file"""
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    return os.path.join(pj_path, "config.yaml")


def get_locale_path() -> str:
    """returns the path to the locale folder"""
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    return os.path.join(pj_path, "locale")


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

        # Get the available languages
        languages: list[str] = []
        for lang in os.listdir(get_locale_path()):
            if os.path.isdir(os.path.join(get_locale_path(), lang)):
                languages.append(lang)
        languages.append("en_US")

        # Print the available languages
        while True:
            clear_console()
            print("Available languages:")

            for i, lang in enumerate(languages):
                print(f"{i + 1}. {lang}")

            # Get the user input
            choice: int = 0
            try:
                users_choice: int = int(
                    input(
                        self.gettext(
                            "Enter the number of the language you want to use: "
                        )
                    )
                )
                if users_choice < 1 or users_choice > len(languages):
                    raise ValueError()
                choice = users_choice
            except ValueError:
                print(self.gettext("Invalid choice. Please try again."))

            # Change the language
            if choice == len(languages):
                self.config.language = "en_US"
                break

            self.config.language = languages[choice - 1]
            break

        save_config_to_file(self.config, get_config_path())
        self.load_gettext()

    def change_tvdb_credentials(self) -> None:
        """
        Changes the TVDB credentials of the application.
        """

        clear_console()
        self.config.tvdb.api_key = input(self.gettext("Enter the TVDB API key: "))
        self.config.tvdb.api_pin = input(self.gettext("Enter the TVDB API pin: "))

        print(self.gettext("TVDB credentials changed successfully."))

        save_config_to_file(self.config, get_config_path())

    def add_plex_librarie(self) -> None:
        """
        Adds a Plex library to the config.
        """
        print("change_plex_libraries()")
        input(self.gettext("Press Enter to continue..."))

    def remove_plex_librarie(self) -> None:
        """
        Removes a Plex library from the config.
        """
        print("change_plex_libraries()")
        input(self.gettext("Press Enter to continue..."))

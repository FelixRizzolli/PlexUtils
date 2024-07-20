"""
This module contains the SettingsConsoleMenu class which is used to create and manage the settings
menu in the console.
"""

import os
from typing import Optional

from plexutils.config.plex_library_infos import PlexLibraryInfos, PlexLibraryType
from plexutils.console.menu import ConsoleMenu, clear_console
from plexutils.shared.config_tools import save_config_to_file


def get_config_path() -> str:
    """
    returns the path to the config file

    :return: The path to the config file
    :rtype: str
    """
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    return os.path.join(pj_path, "config.yaml")


def get_locale_path() -> str:
    """
    returns the path to the locale folder

    :return: The path to the locale folder
    :rtype: str
    """
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

    def setup_menu(self) -> None:
        """
        sets up the menu items

        :return: None
        """
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
                "action": self.add_plex_librarie,
            }
        )
        self.add_item(
            {
                "id": "4",
                "name": self.gettext("Remove a Plex Library"),
                "action": self.remove_plex_librarie,
            }
        )

    def get_utils_name(self) -> str:
        """
        returns the utils name

        :return: The utils name
        :rtype: str
        """
        return self.gettext("Settings")

    def change_language(self) -> None:
        """
        Changes the language of the application.

        :return: None
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

        :return: None
        """

        clear_console()
        self.config.tvdb.api_key = input(self.gettext("Enter the TVDB API key: "))
        self.config.tvdb.api_pin = input(self.gettext("Enter the TVDB API pin: "))
        save_config_to_file(self.config, get_config_path())

        print(self.gettext("TVDB credentials changed successfully."))

    def add_plex_librarie(self) -> None:
        """
        Adds a Plex library to the config.

        :return: None
        """
        clear_console()

        lib_name = input(self.gettext("Enter the name of the library: "))
        lib_path = input(self.gettext("Enter the path of the library: "))
        lib_type = None
        while True:
            # Print the available library types
            plex_library_types: list[str] = [
                library_type.value for library_type in PlexLibraryType
            ]
            print(self.gettext("Available library types:"))
            for i, library_type in enumerate(plex_library_types):
                print(f"{i + 1}. {library_type}")

            # Get the user input
            try:
                users_choice: int = int(
                    input(self.gettext("Enter the number of the library type: "))
                )

                # Check if the user input is valid
                if users_choice < 1 or users_choice > len(plex_library_types):
                    raise ValueError()

                # Set the library type
                if users_choice == 1:
                    lib_type = PlexLibraryType.MOVIE
                else:
                    lib_type = PlexLibraryType.TVSHOW
                break
            except ValueError:
                print(self.gettext("Invalid choice. Please try again."))
                continue
        lib_dub_lang = input(self.gettext("Enter the dub language of the library: "))
        lib_sub_lang = input(self.gettext("Enter the sub language of the library: "))

        new_library: PlexLibraryInfos = PlexLibraryInfos(
            type=lib_type,
            name=lib_name,
            path=lib_path,
            dub_lang=lib_dub_lang,
            sub_lang=lib_sub_lang,
        )
        self.config.libraries.append(new_library)
        save_config_to_file(self.config, get_config_path())

        print(self.gettext("Library added successfully."))

    def remove_plex_librarie(self) -> None:
        """
        Removes a Plex library from the config.

        :return: None
        """
        clear_console()

        # Print the available libraries
        print(self.gettext("Available libraries:"))
        for i, lib in enumerate(self.config.libraries):
            print(f"{i + 1}. {lib.name}")

        # Get the user input
        choice: int = 0
        try:
            users_choice: int = int(
                input(
                    self.gettext("Enter the number of the library you want to remove: ")
                )
            )
            if users_choice < 1 or users_choice > len(self.config.libraries):
                raise ValueError()
            choice = users_choice
        except ValueError:
            print(self.gettext("Invalid choice. Please try again."))
            return

        # Remove the library
        self.config.libraries.pop(choice - 1)
        save_config_to_file(self.config, get_config_path())

        print(self.gettext("Library removed successfully."))

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a warning message if needed.

        :return: A warning message if needed, None otherwise.
        :rtype: Optional[str]
        """
        return None

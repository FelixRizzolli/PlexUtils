"""
This module provides the Menu class which is used to create and manipulate a menu with a list
of options.
"""

import os
from typing import Any, Callable, Optional

from plexutils.config.config import Config
from plexutils.shared.config_tools import load_config, setup_i18n


def clear_console() -> None:
    """
    Clears the console screen. This function doesn't work in IDEs like PyCharm.

    :return: None
    """
    print("clear_console()")
    command: str = "cls" if os.name == "nt" else "clear"
    os.system(command)


class ConsoleMenu:
    """
    The Menu class represents a menu with a list of options.
    """

    config: Config
    gettext: Callable[[str], str]

    title: str = ""
    menu_list: list[dict] = []
    is_main_menu: bool = False

    def __init__(self, is_main_menu: bool = False):
        """
        Initializes a new instance of the Menu class.

        :param is_main_menu: A boolean value indicating whether the menu is the main menu.
        :type is_main_menu: bool
        """

        # Load the configuration
        self.config = load_config()

        # Setup internationalization
        self.load_gettext()

        # Initialize the menu
        self.menu_list = []
        self.is_main_menu = is_main_menu

    def id_exists(self, option_id: str) -> bool:
        """
        Checks if an option with the given id exists in the menu.

        :param option_id: The id of the option to check.
        :type option_id: str

        :return: True if an option with the given id exists in the menu, False otherwise.
        :rtype: bool
        """

        for item in self.menu_list:
            if item["id"].upper() == option_id.upper():
                return True
        return False

    def get_option_by_id(self, option_id: str) -> Optional[dict]:
        """
        Returns the option with the given id from the menu.

        :param option_id: The id of the option to get.
        :type option_id: str

        :return: The option with the given id if it exists in the menu, None otherwise.
        :rtype: Optional[dict]
        """

        for option in self.menu_list:
            if option["id"].upper() == option_id.upper():
                return option
        return None

    def get_list(self) -> list[dict]:
        """
        Returns the list of menu options.

        :return: The list of menu options.
        :rtype: list[dict]
        """

        return self.menu_list

    def add_item(self, item: dict) -> None:
        """
        Adds a new item to the menu.

        :param item: The item to add to the menu.
        :type item: dict

        :return: None
        """

        self.menu_list.append(item)

    def print_menu(self) -> None:
        """
        Prints the menu and prompts the user to make a choice.

        :return: None
        """

        while True:
            clear_console()

            # Print the title of the menu
            print("\n" + self.title)

            # Print the menu options
            self.print_menu_options()

            # Check the configuration
            warning: Optional[str] = self.check_config()
            if warning is not None:
                print(f"\n ⚠️ {warning} ⚠️")

            # Print a new line before the settings and exit option
            print()

            # Print the settings option
            self.print_settings_option()

            # Print the exit option
            print(self.gettext("E. Exit"))

            # Get the user's choice
            choice: str = input("\n" + self.gettext("Enter your choice: "))

            # Check if the user wants to exit the menu
            if choice.upper() == "E":
                return

            # Perform the action associated with the user's choice
            self.perform_menu_action(choice)

    def print_menu_options(self) -> None:
        """
        Prints the menu options.

        :return: None
        """

        for option in self.get_list():
            if option["id"].upper() == "E":
                raise ValueError(
                    self.gettext("The Option 'E' is reserved for the Exit.")
                )
            if option["id"].upper() == "S" and self.is_main_menu:
                continue

            print(f"{option['id']}. {option['name']}")

    def print_settings_option(self) -> None:
        """
        Prints the settings option in the menu.

        :return: None
        """

        if self.is_main_menu:
            settings_option: Optional[dict[Any, Any]] = self.get_option_by_id("S")
            if settings_option is None:
                raise ValueError(self.gettext("The settings option does not exist."))
            print(f"{settings_option['id']}. {settings_option['name']}")

    def perform_menu_action(self, choice: str) -> None:
        """
        Performs the action associated with the user's choice in the menu.

        :param choice: The user's choice.
        :type choice: str

        :return: None
        """

        # Check if the user wants to go to the settings menu
        if choice.upper() == "S" and self.is_main_menu:
            if self.config is None:
                raise ValueError(
                    self.gettext(
                        "The config object is required to go to the settings menu."
                    )
                )

        # Check if the users choice is a valid option
        if self.id_exists(choice):
            menu_option: Optional[dict] = self.get_option_by_id(choice)

            if menu_option is None:
                raise ValueError(self.gettext("The menu option does not exist."))
            if "action" not in menu_option:
                raise ValueError(
                    self.gettext("The menu option does not have an action.")
                )
            if not callable(menu_option["action"]):
                raise ValueError(self.gettext("The action is not a callable function."))

            menu_option["action"]()
        else:
            print("\n" + self.gettext("Invalid choice. Please enter a valid option."))

    def load_gettext(self) -> None:
        """
        Loads the gettext function for internationalization.

        :return: None
        """
        # Get the path of the script and the project
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")

        # Setup internationalization
        self.gettext = setup_i18n(pj_path, self.config)

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a message.

        :return: A message about the configuration.
        :rtype: Optional[str]
        """
        return None

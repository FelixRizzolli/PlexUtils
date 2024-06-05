"""
This module contains utility functions for handling console menus in a Plex server setup.
These functions are primarily used for displaying menus, handling user input, and executing
associated actions.
"""

import os
from typing import Callable, Optional

from plexutils.config.config import Config
from plexutils.shared.console_menu import ConsoleMenu


def clear_console() -> None:
    """
    Clears the console screen. This function doesn't work in IDEs like PyCharm.

    Returns:
        None
    """
    print("clear_console()")
    command: str = "cls" if os.name == "nt" else "clear"
    os.system(command)


def print_menu(
    title: str,
    gettext: Callable[[str], str],
    menu_list: ConsoleMenu,
    config: Config = None,
) -> None:
    """
    Prints the menu of the given menu list and handles the user input.

    Parameters:
        title (str): The title of the menu.
        gettext (Callable[[str], str]): A function to translate a string into the user's language.
        menu_list (ConsoleMenu): A Menu object that contains the menu options.
        config (Config): A Config object that contains the configuration settings.

    Returns:
        None
    """

    while True:
        clear_console()

        # Print the title of the menu
        print("\n" + title)

        # Print the menu options
        for option in menu_list.get_list():
            print(f"{option['id']}. {option['name']}")

        # Print a new line before the settings option
        print()

        # Print the settings option only if it is the main menu
        if menu_list.is_main_menu:
            print(gettext("S. Settings"))

        # Print the exit option
        print(gettext("E. Exit"))

        # Get the user's choice
        choice: str = input("\n" + gettext("Enter your choice: "))

        # Check if the user wants to exit the menu
        if choice.upper() == "E":
            return

        # Perform the action associated with the user's choice
        perform_menu_action(choice, gettext, menu_list, config)


def perform_menu_action(
    choice: str,
    gettext: Callable[[str], str],
    menu_list: ConsoleMenu,
    config: Config = None,
) -> None:
    """
    Performs the action associated with the user's choice in the menu.
    :param choice: The user's choice.
    :param gettext: The function to translate a string into the user's language.
    :param menu_list: The menu list containing the menu options.
    :param config: The Config object containing the configuration settings.
    :return:
    """

    # Check if the user wants to go to the settings menu
    if choice.upper() == "S" and menu_list.is_main_menu:
        if config is None:
            raise ValueError(
                gettext("The config object is required to go to the settings menu.")
            )
        print_settings_menu(gettext)
        return

    # Check if the users choice is a valid option
    if menu_list.id_exists(choice):
        menu_option: Optional[dict] = menu_list.get_option_by_id(choice)

        if menu_option is None:
            raise ValueError(gettext("The menu option does not exist."))
        if "action" not in menu_option:
            raise ValueError(gettext("The menu option does not have an action."))
        if not callable(menu_option["action"]):
            raise ValueError(gettext("The action is not a callable function."))

        menu_option["action"]()
    else:
        print("\n" + gettext("Invalid choice. Please enter a valid option."))


def print_settings_menu(gettext: Callable[[str], str]) -> None:
    """
    Prints the Settings Menu
    :param gettext: A function to translate a string into the user's language.
    :return:
    """
    menu_list: ConsoleMenu = ConsoleMenu(
        menu_list=[
            {"id": "1", "name": gettext("Change Language")},
            {"id": "2", "name": gettext("Change Theme")},
        ],
    )
    print_menu(gettext("Settings Menu"), gettext, menu_list)


def print_library_menu(gettext: Callable[[str], str], menu_list: ConsoleMenu) -> str:
    """
    Prints a library menu and prompts the user to make a choice.
    It keeps prompting until a valid choice is made.

    Parameters:
        gettext (Callable[[str], str]): A function to translate a string into
                                        the user's language.
        menu_list (ConsoleMenu): A Menu object that contains the menu options.

    Returns:
        str: The path associated with the chosen option from the menu.
    """

    while True:
        clear_console()
        print("\n" + gettext("Library Menu"))
        for option in menu_list.get_list():
            print(f"{option['id']}. {option['name']}")

        choice: str = input("\n" + gettext("Enter your choice: "))

        if menu_list.id_exists(choice):
            menu_option: Optional[dict] = menu_list.get_option_by_id(choice)

            if menu_option is None:
                raise ValueError("The menu option does not exist.")

            return menu_option["path"]

        print("\n" + gettext("Invalid choice. Please enter a valid option."))


def library_menu_wrapper(
    gettext: Callable[[str], str],
    config: Config,
    library_type: str,
    fun: Callable[[str], None],
) -> None:
    """
    This function wraps the process of displaying a library menu, getting user input, and
    executing a function with the selected library's path.

    Parameters:
        gettext (Callable[[str], str]): A function to translate a string into the user's
                                        language.
        config (Config): A Config object that contains the configuration settings.
        library_type (str): The type of library (e.g., 'movie', 'tvshow') to display in
                            the menu.
        fun (Callable[[str], None]): A function to execute with the selected library's path
                                     as an argument.

    Returns:
        None
    """
    library_menu = ConsoleMenu([])

    option_id: int = 0
    for lib in config.libraries:
        if lib.type != library_type:
            continue

        option_id += 1
        lib_obj = {
            "id": str(option_id),
            "name": get_library_name(lib.name, lib.dub_lang, lib.sub_lang),
            "path": lib.path,
        }
        library_menu.add_item(lib_obj)

    selected_library = print_library_menu(gettext, library_menu)

    fun(selected_library)


def get_library_name(name: str, dub_lang: str, sub_lang: str) -> str:
    """
    Generates a library name based on the given name, dubbed language, and subtitle
    language.

    Parameters:
        name (str): The name of the library.
        dub_lang (str): The language in which the library is dubbed.
                        It can be a 2-letter or 5-letter language code.
        sub_lang (str): The language in which the subtitles are available.
                        It can be a 2-letter or 5-letter language code.

    Returns:
        str: The library name in the format "(DUB_LANG-SUB_LANG) NAME".
    """

    library_name: str = ""

    if len(dub_lang) == 5:
        library_name += f"({dub_lang[3:5].upper()}"
    elif len(dub_lang) == 2:
        library_name += f"({dub_lang.upper()}"
    else:
        library_name += "(EN"

    if len(sub_lang) == 5:
        library_name += f"-{sub_lang[3:5].upper()})"
    elif len(sub_lang) == 2:
        library_name += f"-{sub_lang.upper()})"
    else:
        library_name += ")"

    library_name += f" {name}"

    return library_name

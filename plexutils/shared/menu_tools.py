"""
This module contains utility functions for handling console menus in a Plex server setup.
These functions are primarily used for displaying menus, handling user input, and executing
associated actions.
"""

import os
from typing import Callable, Optional

from plexutils.shared.menu import Menu


def clear_console() -> None:
    """
    Clears the console screen. This function doesn't work in IDEs like PyCharm.

    Returns:
        None
    """
    print("clear_console()")
    command: str = "cls" if os.name == "nt" else "clear"
    os.system(command)


def print_menu(title: str, gettext: Callable[[str], str], menu_list: Menu) -> None:
    """
    Prints the menu of the given menu list and handles the user input.

    Parameters:
        title (str): The title of the menu.
        gettext (Callable[[str], str]): A function to translate a string into the user's language.
        menu_list (Menu): A Menu object that contains the menu options.

    Returns:
        None
    """
    while True:
        clear_console()
        print("\n" + title)
        for option in menu_list.get_list():
            print(f"{option['id']}. {option['name']}")

        print()
        print(gettext("E. Exit"))

        choice: str = input("\n" + gettext("Enter your choice: "))

        if choice.upper() == "E":
            return

        if menu_list.id_exists(choice):
            menu_option: Optional[dict] = menu_list.get_option_by_id(choice)

            if menu_option is None:
                raise ValueError("The menu option does not exist.")
            if "action" not in menu_option:
                raise ValueError("The menu option does not have an action.")
            if not callable(menu_option["action"]):
                raise ValueError("The action is not a callable function.")

            menu_option["action"]()
        else:
            print("\n" + gettext("Invalid choice. Please enter a valid option."))


def print_library_menu(gettext: Callable[[str], str], menu_list: Menu) -> str:
    """
    Prints a library menu and prompts the user to make a choice.
    It keeps prompting until a valid choice is made.

    Parameters:
        gettext (Callable[[str], str]): A function to translate a string into
                                        the user's language.
        menu_list (Menu): A Menu object that contains the menu options.

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
    config: dict,
    library_type: str,
    fun: Callable[[str], None],
) -> None:
    """
    Creates a menu for a specific type of library and then performs a function on the
    selected library.

    Parameters:
        gettext (Callable[[str], str]): A function to translate a text message into
                                        another language.
        config (dict): A dictionary containing configuration details. It should include
                       details of libraries under the key '<library_type>_libraries'.
        library_type (str): The type of library for which the menu is to be created. It
                            should correspond to a key in the config dictionary.
        fun (Callable): A function that will be called with the selected library as its
                        argument.

    Returns:
        None
    """
    library_menu = Menu([])

    option_id: int = 0
    for lib in config[library_type + "_libraries"]:
        option_id += 1
        lib_obj = {
            "id": str(option_id),
            "name": get_library_name(
                lib["name"], lib["lang"]["dub"], lib["lang"]["sub"]
            ),
            "path": lib["path"],
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

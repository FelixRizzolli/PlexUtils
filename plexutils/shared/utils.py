"""
    This module provides some utility functions.
"""

import gettext as _
import os
import re
from datetime import datetime
from typing import Callable, Optional

import yaml

from plexutils.shared.menu import Menu


def load_config(config_file: str) -> dict:
    """loads the config file from the given directory and returns it as a dict"""
    config: dict = {}
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def setup_i18n(pj_path: str, config: dict) -> Callable[[str], str]:
    """returns the configured gettext"""
    locale_dir: str = os.path.join(pj_path, "locale")

    language: str = "en_US"
    if (config is not None) and ("language" in config):
        language = config["language"]

    trans = _.translation("plexutils", locale_dir, [language], fallback=True)
    trans.install()
    return trans.gettext


def clear_console() -> None:
    """clears the console screen for windows and unix - this doesn't wor in ides like pycharm"""
    print("clear_console()")
    command: str = "cls" if os.name == "nt" else "clear"
    os.system(command)


def print_menu(title: str, gettext: Callable[[str], str], menu_list: Menu) -> None:
    """prints the menu of the given menu list and handles the user input"""
    while True:
        clear_console()
        print("\n" + title)
        for option in menu_list.get_list():
            print(f"{option['id']}. {option['name']}")

        print("\n" + gettext("E. Exit"))

        choice: str = input("\n" + gettext("Enter your choice: "))

        if choice.upper() == "E":
            return

        if menu_list.id_exists(choice):
            menu_list.get_option_by_id(choice)["action"]()
        else:
            print("\n" + gettext("Invalid choice. Please enter a valid option."))


def print_library_menu(gettext: Callable[[str], str], menu_list: Menu) -> str:
    """
    This function prints a library menu and prompts the user to make a choice.
    It keeps prompting until a valid choice is made.

    Parameters:
        gettext (function): A function to translate a string into the user's language.
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
            return menu_list.get_option_by_id(choice)["path"]

        print("\n" + gettext("Invalid choice. Please enter a valid option."))


def library_menu_wrapper(
    gettext: Callable[[str], str],
    config: dict,
    library_type: str,
    fun: Callable[[str], None],
) -> None:
    """
    This function creates a menu for a specific type of library and then performs a function
    on the selected library.

    Parameters:
        gettext (function): A function to translate a text message into another language.
        config (dict): A dictionary containing configuration details. It should include
                       details of libraries under the key '<library_type>_libraries'.
        library_type (str): The type of library for which the menu is to be created. It
                            should correspond to a key in the config dictionary.
        fun (Callable): A function that will be called with the selected library as its argument.

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


def extract_tvdbid(dirname: str) -> Optional[int]:
    """extracts the tvdb id from the given directory string"""
    tvdbid_pattern: str = r"{tvdb-(\d+)}"

    tvdbid_match: Optional[re.Match] = re.search(tvdbid_pattern, dirname)

    if tvdbid_match:
        return int(tvdbid_match.group(1))
    return None


def extract_episodeid(filename: str) -> Optional[int]:
    """extracts the episode id from the given filename"""
    episodeid_pattern: str = r"- s(\d+)e(\d+)"

    episodeid_match: Optional[re.Match] = re.search(episodeid_pattern, filename)

    if episodeid_match:
        return int(episodeid_match.group(2))
    return None


def extract_seasonid_from_episode(filename: str) -> Optional[int]:
    """extracts the season id from the given filename"""
    seasonid_pattern: str = r"- s(\d+)e(\d+)"

    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, filename)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def extract_seasonid(dirname: str) -> Optional[int]:
    """extracts the season id from the given directory string"""
    seasonid_pattern: str = r"season (\d+)"

    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, dirname)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def get_library_name(name: str, dub_lang: str, sub_lang: str) -> str:
    """
    This function generates a library name based on the given name, dubbed language,
    and subtitle language.

    Parameters:
        name (str): The name of the library.
        dub_lang (str): The language in which the library is dubbed. It can be a 2-letter
                        or 5-letter language code.
        sub_lang (str): The language in which the subtitles are available. It can be a 2-letter
                        or 5-letter language code.

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


def is_past_date(iso_date_string: str) -> bool:
    """checks if the given date string is in the past"""
    return not is_future_date(iso_date_string)


def is_future_date(iso_date_string: str) -> bool:
    """checks if the given date string is in the future"""
    # Parse the ISO date string into a datetime object
    date: datetime = datetime.fromisoformat(iso_date_string)

    # Get the current date and time
    now: datetime = datetime.now()

    # Compare the two dates
    if date > now:
        return True
    return False

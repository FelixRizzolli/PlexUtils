"""
    This module provides some utility functions.
"""

import gettext as _
import os
import re
from datetime import datetime
from typing import Callable, Optional

import yaml


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


def print_menu(title, gettext, menu_list) -> None:
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


def extract_tvdbid(dirname) -> Optional[int]:
    """extracts the tvdb id from the given directory string"""
    tvdbid_pattern: str = r"{tvdb-(\d+)}"

    tvdbid_match: Optional[re.Match] = re.search(tvdbid_pattern, dirname)

    if tvdbid_match:
        return int(tvdbid_match.group(1))
    return None


def extract_episodeid(filename) -> Optional[int]:
    """extracts the episode id from the given filename"""
    episodeid_pattern: str = r"- s(\d+)e(\d+)"

    episodeid_match: Optional[re.Match] = re.search(episodeid_pattern, filename)

    if episodeid_match:
        return int(episodeid_match.group(2))
    return None


def extract_seasonid_from_episode(filename) -> Optional[int]:
    """extracts the season id from the given filename"""
    seasonid_pattern: str = r"- s(\d+)e(\d+)"

    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, filename)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def extract_seasonid(dirname) -> Optional[int]:
    """extracts the season id from the given directory string"""
    seasonid_pattern: str = r"season (\d+)"

    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, dirname)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def is_past_date(iso_date_string) -> bool:
    """checks if the given date string is in the past"""
    return not is_future_date(iso_date_string)


def is_future_date(iso_date_string) -> bool:
    """checks if the given date string is in the future"""
    # Parse the ISO date string into a datetime object
    date: datetime = datetime.fromisoformat(iso_date_string)

    # Get the current date and time
    now: datetime = datetime.now()

    # Compare the two dates
    if date > now:
        return True
    return False

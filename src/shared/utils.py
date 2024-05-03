import os
import re

import yaml

from menu import clear_console

def load_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def print_menu(title, gettext, menu_list):
    while True:
        clear_console()
        print("\n" + title)
        for option in menu_list.get_list():
            print(f"{option["id"]}. {option["name"]}")

        print("\n" + gettext("E. Exit"))

        choice = input("\n" + gettext("Enter your choice: "))

        if choice.upper() == "E":
            return

        if menu_list.id_exists(choice):
            menu_list.get_option_by_id(choice)["action"]()
        else:
            print("\n" + gettext("Invalid choice. Please enter a valid option."))


def extract_tvdbid(dirname):
    tvdbid_pattern = r'{tvdb-(\d+)}'

    tvdbid_match = re.search(tvdbid_pattern, dirname)

    if tvdbid_match:
        return int(tvdbid_match.group(1))
    else:
        return None


def extract_episodeid(filename):
    episodeid_pattern = r'- s(\d+)e(\d+)'

    episodeid_match = re.search(episodeid_pattern, filename)

    if episodeid_match:
        return int(episodeid_match.group(2))
    else:
        return None


def extract_seasonid_from_episode(filename):
    seasonid_pattern = r'- s(\d+)e(\d+)'

    seasonid_match = re.search(seasonid_pattern, filename)

    if seasonid_match:
        return int(seasonid_match.group(1))
    else:
        return None


def extract_seasonid(dirname):
    seasonid_pattern = r'season (\d+)'

    seasonid_match = re.search(seasonid_pattern, dirname)

    if seasonid_match:
        return int(seasonid_match.group(1))
    else:
        return None


def delete_directory(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)
    os.rmdir(dir_path)
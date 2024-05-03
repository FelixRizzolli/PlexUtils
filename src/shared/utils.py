import re

from menu import clear_console


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

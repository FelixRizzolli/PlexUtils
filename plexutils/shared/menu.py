"""
This module provides the Menu class which is used to create and manipulate a menu with a list
of options.
"""

from typing import Optional


class Menu:
    """
    The Menu class represents a menu with a list of options.

    Attributes:
        menu_list (list[dict]): A list of dictionaries where each dictionary represents a menu item.

    Methods:
        __init__(self, menu_list: list[dict]): Initializes a new instance of the Menu class.
        id_exists(self, option_id: str): Checks if an option with the given id exists in the menu.
        get_option_by_id(self, option_id: str): Returns the option with the given id from the menu.
        get_list(self): Returns the list of menu options.
        add_item(self, item): Adds a new item to the menu.
    """

    def __init__(self, menu_list: list[dict]):
        """
        Initializes a new instance of the Menu class.

        Parameters:
            menu_list (list[dict]): A list of dictionaries where each dictionary represents a
                                    menu item.
        """

        self.menu_list: list[dict] = menu_list

    def id_exists(self, option_id: str) -> bool:
        """
        Checks if an option with the given id exists in the menu.

        Parameters:
            option_id (str): The id of the option to check.

        Returns:
            bool: True if an option with the given id exists in the menu, False otherwise.
        """

        for item in self.menu_list:
            if item["id"] == option_id:
                return True
        return False

    def get_option_by_id(self, option_id: str) -> Optional[dict]:
        """
        Returns the option with the given id from the menu.

        Parameters:
            option_id (str): The id of the option to get.

        Returns:
            dict: The option with the given id if it exists in the menu, None otherwise.
        """

        for option in self.menu_list:
            if option["id"] == option_id:
                return option
        return None

    def get_list(self) -> list[dict]:
        """
        Returns the list of menu options.

        Returns:
            list[dict]: The list of menu options.
        """

        return self.menu_list

    def add_item(self, item) -> None:
        """
        Adds a new item to the menu.

        Parameters:
            item (dict): The item to add to the menu.
        """

        self.menu_list.append(item)

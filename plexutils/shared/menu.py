"""
    This module contains Menu class.
"""

from typing import Optional


class Menu:
    """class for working with menu items"""

    def __init__(self, menu_list: list[dict]):
        self.menu_list: list[dict] = menu_list

    def id_exists(self, option_id: str) -> bool:
        """returns true if option with the id option_id exists in menu"""
        for item in self.menu_list:
            if item["id"] == option_id:
                return True
        return False

    def get_option_by_id(self, option_id: str) -> Optional[dict]:
        """returns the option with the id option_id, if it does not exist than it returns None"""
        for option in self.menu_list:
            if option["id"] == option_id:
                return option
        return None

    def get_list(self) -> list[dict]:
        """returns the menu list"""
        return self.menu_list

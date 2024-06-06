"""
    This module contains unit tests for the Menu class.
"""

import unittest

from plexutils.console.menu import ConsoleMenu


class TestMenu(unittest.TestCase):
    """test class for the Menu class"""

    def setUp(self) -> None:
        self.menu: list[dict] = [
            {"id": "1", "name": "Option 1"},
            {"id": "2", "name": "Option 2"},
            {"id": "3", "name": "Option 3"},
        ]
        self.console_menu: ConsoleMenu = ConsoleMenu()
        self.console_menu.title = "Test Menu:"
        for item in self.menu:
            self.console_menu.add_item(item)

    def test_id_exists(self) -> None:
        """tests the id_exists method"""
        self.assertTrue(self.console_menu.id_exists("1"))
        self.assertFalse(self.console_menu.id_exists("4"))

    def test_get_option_by_id(self) -> None:
        """tests the get_option_by_id method"""
        self.assertEqual(
            self.console_menu.get_option_by_id("1"), {"id": "1", "name": "Option 1"}
        )
        self.assertIsNone(self.console_menu.get_option_by_id("4"))

    def test_get_list(self) -> None:
        """tests the get_list method"""
        self.assertEqual(self.console_menu.get_list(), self.menu)


if __name__ == "__main__":
    unittest.main()

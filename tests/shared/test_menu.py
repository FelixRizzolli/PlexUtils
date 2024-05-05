"""
    This module contains unit tests for the Menu class.
"""
import unittest
from typing import List

from plexutils.shared.menu import Menu


class TestMenu(unittest.TestCase):
    """test class for the Menu class"""

    def setUp(self) -> None:
        self.menu: List[dict] = [
            {'id': '1', 'name': 'Option 1'},
            {'id': '2', 'name': 'Option 2'},
            {'id': '3', 'name': 'Option 3'}
        ]
        self.console_menu: Menu = Menu(self.menu)

    def test_id_exists(self) -> None:
        """tests the id_exists method"""
        self.assertTrue(self.console_menu.id_exists('1'))
        self.assertFalse(self.console_menu.id_exists('4'))

    def test_get_option_by_id(self) -> None:
        """tests the get_option_by_id method"""
        self.assertEqual(self.console_menu.get_option_by_id('1'), {'id': '1', 'name': 'Option 1'})
        self.assertIsNone(self.console_menu.get_option_by_id('4'))

    def test_get_list(self) -> None:
        """tests the get_list method"""
        self.assertEqual(self.console_menu.get_list(), self.menu)


if __name__ == '__main__':
    unittest.main()

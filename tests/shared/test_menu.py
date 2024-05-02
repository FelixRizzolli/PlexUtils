import unittest
from shared.menu import Menu


def action1():
    print("action1")


def actionB():
    print("actionB")


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.menu = [
            {'id': 1, 'name': 'Option 1'},
            {'id': 2, 'name': 'Option 2'},
            {'id': 3, 'name': 'Option 3'}
        ]
        self.console_menu = Menu(self.menu)

    def test_id_exists(self):
        self.assertTrue(self.console_menu.id_exists(1))
        self.assertFalse(self.console_menu.id_exists(4))

    def test_get_option_by_id(self):
        self.assertEqual(self.console_menu.get_option_by_id(1), {'id': 1, 'name': 'Option 1'})
        self.assertIsNone(self.console_menu.get_option_by_id(4))

    def test_get_list(self):
        self.assertEqual(self.console_menu.get_list(), self.menu)


if __name__ == '__main__':
    unittest.main()

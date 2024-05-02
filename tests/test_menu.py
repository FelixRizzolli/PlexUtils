import unittest
from menu import Menu


def action1():
    print("action1")


def actionB():
    print("actionB")


class TestMenu(unittest.TestCase):
    def test_menu_option1(self):
        menu = Menu([
            {"id": "1", "name": "Option 1", "action": action1},
        ])
        self.assertTrue(menu.id_exists("1"))
        self.assertEqual(menu.get_option_by_id("1")["name"], "Option 1")
        self.assertEqual(menu.get_option_by_id("1")["action"], action1)

    def test_menu_optionB(self):
        menu = Menu([
            {"id": "1", "name": "Option 1", "action": action1},
            {"id": "B", "name": "Option B", "action": actionB},
        ])
        self.assertTrue(menu.id_exists("B"))
        self.assertEqual(menu.get_option_by_id("B")["name"], "Option B")
        self.assertEqual(menu.get_option_by_id("B")["action"], actionB)


if __name__ == '__main__':
    unittest.main()

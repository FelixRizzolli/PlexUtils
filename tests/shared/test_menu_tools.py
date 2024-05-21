"""
This module contains unit tests for the functions in the menu_tools.py module.
"""

import unittest
from plexutils.shared.menu_tools import get_library_name


class TestMenuTools(unittest.TestCase):
    """
    This class contains unit tests for the functions in the menu_tools.py module.
    """

    def test_get_library_name_with_dubblank_subblank(self):
        """
        Test case for the `get_library_name` function when both dubbed language and subtitle
        language are blank.
        """
        library_name = get_library_name("Movies", "", "")
        self.assertEqual(library_name, "(EN) Movies")

    def test_get_library_name_with_dubblank_sub2(self):
        """
        Test case for the `get_library_name` function when dubbed language is blank and subtitle
        language is a 2-letter language code.
        """
        library_name = get_library_name("Movies", "", "DE")
        self.assertEqual(library_name, "(EN-DE) Movies")

    def test_get_library_name_with_dubblank_sub5(self):
        """
        Test case for the `get_library_name` function when dubbed language is blank and subtitle
        language is a 5-letter language code.
        """
        library_name = get_library_name("Movies", "", "de_AT")
        self.assertEqual(library_name, "(EN-AT) Movies")

    def test_get_library_name_with_dub2_subblank(self):
        """
        Test case for the `get_library_name` function when dubbed language is a 2-letter language
        code and subtitle language is blank.
        """
        library_name = get_library_name("Movies", "DE", "")
        self.assertEqual(library_name, "(DE) Movies")

    def test_get_library_name_with_dub2_sub2(self):
        """
        Test case for the `get_library_name` function when both dubbed language and subtitle
        language are 2-letter language codes.
        """
        library_name = get_library_name("Movies", "DE", "DE")
        self.assertEqual(library_name, "(DE-DE) Movies")

    def test_get_library_name_with_dub2_sub5(self):
        """
        Test case for the `get_library_name` function when dubbed language is a 2-letter language
        code and subtitle language is a 5-letter language code.
        """
        library_name = get_library_name("Movies", "DE", "de_AT")
        self.assertEqual(library_name, "(DE-AT) Movies")

    def test_get_library_name_with_dub5_subblank(self):
        """
        Test case for the `get_library_name` function when dubbed language is a 5-letter language
        code and subtitle language is blank.
        """
        library_name = get_library_name("Movies", "de_AT", "")
        self.assertEqual(library_name, "(AT) Movies")

    def test_get_library_name_with_dub5_sub2(self):
        """
        Test case for the `get_library_name` function when dubbed language is a 5-letter language
        code and subtitle language is a 2-letter language code.
        """
        library_name = get_library_name("Movies", "de_AT", "DE")
        self.assertEqual(library_name, "(AT-DE) Movies")

    def test_get_library_name_with_dub5_sub5(self):
        """
        Test case for the `get_library_name` function when both dubbed language and subtitle
        language are 5-letter language codes.
        """
        library_name = get_library_name("Movies", "de_AT", "de_AT")
        self.assertEqual(library_name, "(AT-AT) Movies")


if __name__ == "__main__":
    unittest.main()

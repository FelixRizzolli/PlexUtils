"""
This module contains unit tests for the functions in the `config_tools.py` module.
These tests are designed to ensure that the configuration loading and internationalization
setup functions are working as expected.
"""

import os
import unittest
from typing import Callable

from plexutils.shared.config_tools import load_config, setup_i18n


def get_config_file(config_id: str) -> str:
    """
    Returns the path to the test configuration file with the given ID.

    :param config_id: The ID of the test configuration file.
    :return: The path to the test configuration file.
    """
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    configs_path: str = os.path.join(pj_path, "data", "config")
    config_file: str = os.path.join(configs_path, f"test_config_{config_id}.yaml")
    return config_file


class TestConfigTools(unittest.TestCase):
    """
    This class contains unit tests for the functions in the config_tools.py module.
    """

    def test_load_config_language_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the language is correctly set to "de_DE".
        """
        congig_file: str = get_config_file("01")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get("language"))
        if config.get("language") is not None:
            self.assertEqual("de_DE", config.get("language"))

    def test_load_config_language_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the language is correctly set to "de_AT".
        """
        congig_file: str = get_config_file("02")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get("language"))
        if config.get("language") is not None:
            self.assertEqual("de_AT", config.get("language"))

    def test_load_config_movie_libraries_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the movie libraries are correctly set.
        """
        congig_file: str = get_config_file("01")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get("movie_libraries"))
        if config.get("movie_libraries") is not None:
            self.assertEqual(2, len(config.get("movie_libraries")))

    def test_load_config_movie_libraries_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the movie libraries are correctly set.
        """
        congig_file: str = get_config_file("02")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNone(config.get("movie_libraries"))

    def test_load_config_tvshow_libraries_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the tvshow libraries are correctly set.
        """
        congig_file: str = get_config_file("01")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get("tvshow_libraries"))
        if config.get("tvshow_libraries") is not None:
            self.assertEqual(2, len(config.get("tvshow_libraries")))

    def test_load_config_mtvshow_libraries_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the tvshow libraries are correctly set.
        """
        congig_file: str = get_config_file("02")
        config: dict = load_config(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get("tvshow_libraries"))
        if config.get("tvshow_libraries") is not None:
            self.assertEqual(1, len(config.get("tvshow_libraries")))

    def test_setup_i18n_deat(self):
        """
        Test case for the `setup_i18n` function. It tests the function with
        a mock configuration dictionary and a mock translation function.
        """
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")

        gettext: Callable[[str], str] = setup_i18n(pj_path, {"language": "de_AT"})

        self.assertEqual(
            "Druck Enter um weiterzugean...", gettext("Press Enter to continue...")
        )
        self.assertEqual("Gib deine Auswohl ein: ", gettext("Enter your choice: "))
        self.assertEqual("E. Ausi", gettext("E. Exit"))

    def test_setup_i18n_dede(self):
        """
        Test case for the `setup_i18n` function. It tests the function with
        a mock configuration dictionary and a mock translation function.
        """
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")

        gettext: Callable[[str], str] = setup_i18n(pj_path, {"language": "de_DE"})

        self.assertEqual(
            "Drücken Sie Enter, um fortzufahren...",
            gettext("Press Enter to continue..."),
        )
        self.assertEqual("Wähle: ", gettext("Enter your choice: "))
        self.assertEqual("E. Exit", gettext("E. Exit"))


if __name__ == "__main__":
    unittest.main()

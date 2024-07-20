"""
This module contains unit tests for the functions in the `config_tools.py` module.
These tests are designed to ensure that the configuration loading and internationalization
setup functions are working as expected.
"""

import os
import unittest
from typing import Callable

from plexutils.config.config import Config
from plexutils.config.tvdb_credentials import TVDBCredentials
from plexutils.shared.config_tools import (
    load_config_from_file,
    parse_config,
    setup_i18n,
)


def get_config_file(config_id: str) -> str:
    """
    Returns the path to the test configuration file with the given ID.

    :param config_id: The ID of the test configuration file.
    :type config_id: str

    :return: The path to the test configuration file.
    :rtype: str
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

    def test_load_config_from_file_language_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the language is correctly set to "de_DE".
        """
        congig_file: str = get_config_file("01")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.language)
        if config.language is not None:
            self.assertEqual("de_DE", config.language)

    def test_load_config_from_file_language_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the language is correctly set to "de_AT".
        """
        congig_file: str = get_config_file("02")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.language)
        if config.language is not None:
            self.assertEqual("de_AT", config.language)

    def test_load_config_from_file_get_movie_libraries_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the movie libraries are correctly set.
        """
        congig_file: str = get_config_file("01")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get_movie_libraries())
        if config.get_movie_libraries() is not None:
            self.assertEqual(2, len(config.get_movie_libraries()))

    def test_load_config_from_file_get_movie_libraries_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the movie libraries are correctly set.
        """
        congig_file: str = get_config_file("02")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertEqual([], config.get_movie_libraries())

    def test_load_config_from_file_get_tvshow_libraries_01(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the tvshow libraries are correctly set.
        """
        congig_file: str = get_config_file("01")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get_tvshow_libraries())
        if config.get_tvshow_libraries() is not None:
            self.assertEqual(2, len(config.get_tvshow_libraries()))

    def test_load_config_from_file_get_tvshow_libraries_02(self):
        """
        Test case for the `load_config` function. It tests the function with
        a mock configuration file and checks if the tvshow libraries are correctly set.
        """
        congig_file: str = get_config_file("02")
        config: Config = load_config_from_file(congig_file)

        self.assertIsNotNone(config)
        self.assertIsNotNone(config.get_tvshow_libraries())
        if config.get_tvshow_libraries() is not None:
            self.assertEqual(1, len(config.get_tvshow_libraries()))

    def test_parse_config_valid(self):
        """
        Test case for the `parse_config` function. It tests the function with
        a valid configuration dictionary.
        """
        config_dict = {
            "language": "en_US",
            "libraries": [
                {
                    "type": "movie",
                    "name": "Movies1",
                    "path": "/path/to/movies1",
                    "dub_lang": "en",
                    "sub_lang": "fr",
                },
                {
                    "type": "tvshow",
                    "name": "TVShows1",
                    "path": "/path/to/tvshows1",
                    "dub_lang": "en",
                    "sub_lang": "fr",
                },
            ],
            "tvdb": {
                "api_key": "your_api_key",
                "api_pin": "your_api_pin",
            },
        }
        config = parse_config(config_dict)

        self.assertIsNotNone(config)
        self.assertEqual("en_US", config.language)
        self.assertEqual(2, len(config.libraries))
        self.assertEqual("your_api_key", config.tvdb.api_key)
        self.assertEqual("your_api_pin", config.tvdb.api_pin)

    def test_parse_config_invalid_language(self):
        """
        Test case for the `parse_config` function. It tests the function with
        an invalid language in the configuration dictionary.
        """
        config_dict = {
            "language": "invalid_language",
            "libraries": [],
            "tvdb": {
                "api_key": "your_api_key",
                "api_pin": "your_api_pin",
            },
        }

        with self.assertRaises(ValueError):
            parse_config(config_dict)

    def test_setup_i18n_deat(self):
        """
        Test case for the `setup_i18n` function. It tests the function with
        a mock configuration dictionary and a mock translation function.
        """
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")

        gettext: Callable[[str], str] = setup_i18n(
            pj_path,
            Config(language="de_AT", libraries=[], tvdb=TVDBCredentials("", "")),
        )

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

        gettext: Callable[[str], str] = setup_i18n(
            pj_path,
            Config(language="de_DE", libraries=[], tvdb=TVDBCredentials("", "")),
        )

        self.assertEqual(
            "Drücken Sie Enter, um fortzufahren...",
            gettext("Press Enter to continue..."),
        )
        self.assertEqual("Wähle: ", gettext("Enter your choice: "))
        self.assertEqual("E. Exit", gettext("E. Exit"))


if __name__ == "__main__":
    unittest.main()

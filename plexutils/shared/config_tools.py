"""
This module contains utility functions for handling configuration in a Plex server setup.
These functions are primarily used for loading configuration from a YAML file and setting
up internationalization (i18n).
"""

import gettext as _
import os
from typing import Callable

import yaml


def load_config(config_file: str) -> dict:
    """
    Loads the configuration from a YAML file.

    Parameters:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The configuration dictionary.
    """
    config: dict = {}

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def setup_i18n(pj_path: str, config: dict) -> Callable[[str], str]:
    """
    Sets up internationalization (i18n) using the given project path and configuration.

    The function uses the 'language' key from the configuration to set the language for i18n.
    If the 'language' key is not found in the configuration, it defaults to 'en_US'.

    Parameters:
        pj_path (str): The path to the project directory.
        config (dict): The configuration dictionary.

    Returns:
        Callable[[str], str]: A function that can be used to translate a string into the
                              configured language.
    """
    locale_dir: str = os.path.join(pj_path, "locale")

    language: str = "en_US"
    if (config is not None) and ("language" in config):
        language = config["language"]

    trans = _.translation("plexutils", locale_dir, [language], fallback=True)
    trans.install()
    return trans.gettext

"""
This module contains utility functions for handling configuration in a Plex server setup.
These functions are primarily used for loading configuration from a YAML file and setting
up internationalization (i18n).
"""

import gettext as _
import os
import re
from typing import Callable

import yaml

from plexutils.config.config import Config
from plexutils.config.plex_library_infos import PlexLibraryInfos, PlexLibraryType
from plexutils.config.tvdb_credentials import TVDBCredentials


def load_config() -> Config:
    """
    Loads the configuration from a YAML file.

    :return: The configuration object.
    :rtype: Config
    """
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    config_file: str = os.path.join(pj_path, "config.yaml")

    return load_config_from_file(config_file)


def load_config_from_file(config_file: str) -> Config:
    """
    Loads the configuration from a YAML file.

    :param config_file: The path to the configuration file.
    :type config_file: str

    :return: The configuration object.
    :rtype: Config
    """
    config_dict: dict = {}

    with open(config_file, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)

    return parse_config(config_dict)


def save_config_to_file(config: Config, config_file: str) -> None:
    """
    Saves the configuration to a YAML file.

    :param config: The configuration object.
    :type config: Config
    :param config_file: The path to the configuration file.
    :type config_file: str

    :return: None
    """
    config_dict: dict = {
        "language": config.language,
        "libraries": [lib.to_dict() for lib in config.libraries],
        "tvdb": config.tvdb.to_dict(),
    }

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_dict, f)


def parse_config(config_dict: dict) -> Config:
    """
    Parses the configuration dictionary and returns a Config object.

    :param config_dict: The configuration dictionary.
    :type config_dict: dict

    :return: The configuration object.
    :rtype: Config
    """
    language: str = "en_US"
    libraries: list[PlexLibraryInfos] = []
    tvdb: TVDBCredentials = TVDBCredentials("", "")

    if "language" in config_dict:
        lang = config_dict["language"]
        lang_pattern = r"^[a-z]{2}_[A-Z]{2}$"
        if not re.match(lang_pattern, lang):
            raise ValueError(f"Invalid language code: {lang}")
        language = lang

    if "libraries" in config_dict:
        libraries = [parse_plex_library_infos(lib) for lib in config_dict["libraries"]]

    if "tvdb" in config_dict:
        tvdb_api_key = config_dict["tvdb"]["api_key"]
        tvdb_api_pin = config_dict["tvdb"]["api_pin"]
        tvdb = TVDBCredentials(tvdb_api_key, tvdb_api_pin)

    return Config(language=language, libraries=libraries, tvdb=tvdb)


def parse_plex_library_infos(config_dict: dict) -> PlexLibraryInfos:
    """
    Parses the configuration dictionary and returns a PlexLibraryInfos object.

    :param config_dict: The configuration dictionary.
    :type config_dict: dict

    :return: The PlexLibraryInfos object.
    :rtype: PlexLibraryInfos
    """
    # Check for required keys
    if "type" not in config_dict:
        raise ValueError("Missing 'type' key in configuration dictionary")
    if "name" not in config_dict:
        raise ValueError("Missing 'name' key in configuration dictionary")
    if "path" not in config_dict:
        raise ValueError("Missing 'path' key in configuration dictionary")

    # Check the dubbing language
    dub_lang: str = ""
    if "lang" in config_dict and "dub" in config_dict["lang"]:
        dub_lang = config_dict["lang"]["dub"]

    # Check the subtitle language
    sub_lang: str = ""
    if "lang" in config_dict and "sub" in config_dict["lang"]:
        sub_lang = config_dict["lang"]["sub"]

    # Parse the library type
    library_type = None
    if config_dict["type"] == "movie":
        library_type = PlexLibraryType.MOVIE
    elif config_dict["type"] == "tvshow":
        library_type = PlexLibraryType.TVSHOW

    # Check if the library type is valid
    if library_type is None:
        raise ValueError(f"Invalid library type: {config_dict['type']}")

    # Create the PlexLibraryInfos object
    return PlexLibraryInfos(
        name=config_dict["name"],
        type=library_type,
        path=config_dict["path"],
        dub_lang=dub_lang,
        sub_lang=sub_lang,
    )


def setup_i18n(pj_path: str, config: Config) -> Callable[[str], str]:
    """
    Sets up internationalization (i18n) using the given project path and configuration.

    The function uses the 'language' key from the configuration to set the language for i18n.
    If the 'language' key is not found in the configuration, it defaults to 'en_US'.

    :param pj_path: The path to the project directory.
    :type pj_path: str
    :param config: The configuration dictionary.
    :type config: Config

    :return: A function that can be used to translate a string into the configured language.
    :rtype: Callable[[str], str]
    """
    locale_dir: str = os.path.join(pj_path, "locale")

    language: str = "en_US"
    if config is not None:
        language = config.language

    trans = _.translation("plexutils", locale_dir, [language], fallback=True)
    trans.install()
    return trans.gettext

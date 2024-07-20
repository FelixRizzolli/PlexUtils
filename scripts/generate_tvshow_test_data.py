"""
This module contains functions to generate TV show directories based on a JSON file.
"""

import json
import os


def generate_tvshow_libaries(data_dir: str, scripts_data_dir: str) -> None:
    """
    Generates TV show libraries based on JSON files.

    :param data_dir: The path of the data directory where the TV show directories will be created.
    :type data_dir: str
    :param scripts_data_dir: The path of the scripts data directory where the JSON files are
                             located.
    :type scripts_data_dir: str

    :return: None
    """
    libraries = [
        {"name": "tvshows", "source_file": "tvshow_files.json"},
        {"name": "animes", "source_file": "anime_tvshow_files.json"},
    ]

    tvshows_dir = os.path.join(data_dir, "tvshows")
    if not os.path.isdir(tvshows_dir):
        os.mkdir(tvshows_dir)

    for lib in libraries:
        library_dir = os.path.join(tvshows_dir, lib["name"])
        source_file = os.path.join(scripts_data_dir, "tvshows", lib["source_file"])
        generate_tvshow_library(library_dir, source_file)

    print("Generate tvshow libraries: DONE!")


def generate_tvshow_library(library_dir: str, source_file: str) -> None:
    """
    Generates TV show directories based on a JSON file.

    The function creates directories if they do not exist, then reads a JSON file containing
    TV show directory names. It then creates these TV show directories in the specified directory.

    :param library_dir: The path of the library directory where the TV show directories will be
                        created.
    :type library_dir: str
    :param source_file: The path of the source file where the JSON file is located.
    :type source_file: str

    :return: None
    """
    # Open the JSON file
    print("\nRead tvshow_files.json")
    with open(source_file, "r", encoding="utf-8") as f:
        # Load the JSON data into a Python dictionary
        tvshow_directories = json.load(f)["tvshow_files"]

    # Create library directory
    print(f"Create {library_dir} directory")
    if not os.path.isdir(library_dir):
        os.mkdir(library_dir)

    # Create tvshow directories
    print("Create tvshow files")
    for tvshow in tvshow_directories:
        tvshow_dirname: str = tvshow["dirname"]
        tvshow_dir: str = os.path.join(library_dir, tvshow_dirname)
        print(f"Create files for: {tvshow_dirname}")

        if not os.path.isdir(tvshow_dir):
            os.mkdir(tvshow_dir)

        generate_tvshow_season_directories(tvshow_dir, tvshow)

    print("Generate tvshow files: DONE!")


def generate_tvshow_season_directories(tvshow_dir: str, tvshow: dict) -> None:
    """
    Generates TV show season directories.

    The function creates season directories within a TV show directory.

    :param tvshow_dir: The path of the TV show directory where the season directories will be
                       created.
    :type tvshow_dir: str
    :param tvshow: A dictionary containing information about the TV show and its seasons.
    :type tvshow: dict

    :return: None
    """
    for season in tvshow["seasons"]:
        season_dirname: str = season["dirname"]
        season_dir: str = os.path.join(tvshow_dir, season_dirname)

        if not os.path.isdir(season_dir):
            os.mkdir(season_dir)

        generate_tvshow_episode_files(season_dir, season)


def generate_tvshow_episode_files(season_dir: str, season: dict) -> None:
    """
    Generates TV show episode files.

    The function creates episode files within a season directory.

    :param season_dir: The path of the season directory where the episode files will be created.
    :type season_dir: str
    :param season: A dictionary containing information about the season and its episodes.
    :type season: dict

    :return: None
    """
    for episode in season["episodes"]:
        episode_dir: str = os.path.join(season_dir, episode)

        with open(episode_dir, "a", encoding="utf-8"):
            pass

"""
This module contains functions to generate TV show directories based on a JSON file.
"""
import os
import json


def generate_tvshow_directories(data_dir: str, scripts_data_dir: str) -> None:
    """
    Generates TV show directories based on a JSON file.

    The function creates directories if they do not exist, then reads a JSON file containing
    TV show directory names. It then creates these TV show directories in the specified directory.

    Args:
        data_dir (str): The path of the data directory where the TV show directories will be
                        created.
        scripts_data_dir (str): The path of the scripts data directory where the JSON file is
                                located.
    """
    tvshows_dir = os.path.join(data_dir, 'tvshows')

    # Open the JSON file
    with open(os.path.join(scripts_data_dir, 'tvshow_files.json'), 'r', encoding='utf-8') as f:
        # Load the JSON data into a Python dictionary
        tvshow_directories = json.load(f)['movie_files']

    # Create data
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if not os.path.isdir(tvshows_dir):
        os.mkdir(tvshows_dir)

    # Create tvshow directories
    for tvshow in tvshow_directories:
        tvshow_dirname: str = tvshow["dirname"]
        tvshow_dir: str = os.path.join(tvshows_dir, tvshow_dirname)

        if not os.path.isdir(tvshow_dir):
            os.mkdir(tvshow_dir)

        generate_tvshow_season_directories(tvshow_dir, tvshow)


def generate_tvshow_season_directories(tvshow_dir: str, tvshow: dict) -> None:
    """
    Generates TV show season directories.

    The function creates season directories within a TV show directory.

    Args:
        tvshow_dir (str): The path of the TV show directory where the season directories
                          will be created.
        tvshow (dict): A dictionary containing information about the TV show and its seasons.
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

    Args:
        season_dir (str): The path of the season directory where the episode files will be created.
        season (dict): A dictionary containing information about the season and its episodes.
    """
    for episode in season["episodes"]:
        episode_dir: str = os.path.join(season_dir, episode)

        with open(episode_dir, 'a', encoding='utf-8'):
            pass

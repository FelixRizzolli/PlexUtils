"""
This module contains functions to generate test data for movies and TV shows.
"""

import os

from scripts.generate_movie_test_data import generate_movie_libraries
from scripts.generate_test_config_files import generate_test_config_files
from scripts.generate_tvshow_test_data import generate_tvshow_libaries


def delete_directory(dir_path) -> None:
    """
    Deletes the given directory and all its contents.

    :param dir_path: The path of the directory to be deleted.
    :type dir_path: str

    :return: None
    """
    for item in os.listdir(dir_path):
        item_path: str = os.path.join(dir_path, item)

        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)

    os.rmdir(dir_path)


def generate_test_data() -> None:
    """
    Generates test data for movies and TV shows.

    The function first deletes any existing data in the 'movies' and 'tvshows' directories.
    Then, it generates new movie files and TV show directories.

    :return: None
    """
    # Get the absolute path of the current script
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))

    # Define the path to the 'data' directory
    data_dir: str = os.path.join(current_script_dir, "../data")

    # Define the path to the 'scripts/data' directory
    scripts_data_dir: str = os.path.join(current_script_dir, "data")

    # Delete the 'data' directory
    print("Delete the 'data' directory")
    if os.path.exists(data_dir):
        delete_directory(os.path.join(data_dir))

    # Create the 'data' directory
    print("Create the 'data' directory")
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    # Generate the data
    generate_movie_libraries(data_dir, scripts_data_dir)
    generate_tvshow_libaries(data_dir, scripts_data_dir)
    generate_test_config_files(data_dir, scripts_data_dir)

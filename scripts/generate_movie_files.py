"""
This module contains functions to generate movie files based on a JSON file.
"""
import os
import json


def generate_movie_files(data_dir: str, scripts_data_dir: str) -> None:
    """
    Generates movie files based on a JSON file.

    The function creates directories if they do not exist, then reads a JSON file containing
    movie file names. It then creates these movie files in the specified directory.

    Args:
        data_dir (str): The path of the data directory where the movie files will be created.
        scripts_data_dir (str): The path of the scripts data directory where the JSON file is
                                located.
    """
    movies_dir = os.path.join(data_dir, 'movies')

    # Open the JSON file
    with open(os.path.join(scripts_data_dir, 'movie_files.json'), 'r', encoding='utf-8') as f:
        # Load the JSON data into a Python dictionary
        movie_files = json.load(f)['movie_files']

    # Create directories
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if not os.path.isdir(movies_dir):
        os.mkdir(movies_dir)

    # Create movie files
    for movie_file in movie_files:
        with open(os.path.join(movies_dir, movie_file), 'a', encoding='utf-8'):
            pass

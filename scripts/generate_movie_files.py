import os
import json


def generate_movie_files(data_dir: str, scripts_data_dir: str) -> None:
    movies_dir = os.path.join(data_dir, 'movies')

    # Open the JSON file
    with open(os.path.join(scripts_data_dir, 'movie_files.json'), 'r', encoding='utf-8') as f:
        # Load the JSON data into a Python dictionary
        movie_files = json.load(f)['movie_files']

    # create directories
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if not os.path.isdir(movies_dir):
        os.mkdir(movies_dir)

    # create movie files
    for movie_file in movie_files:
        with open(os.path.join(movies_dir, movie_file), 'a', encoding='utf-8'):
            pass

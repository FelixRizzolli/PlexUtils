import os

from generate_movie_files import generate_movie_files
from generate_tvshow_files import generate_tvshow_files


def delete_directory(dir_path):
    """deletes the given directory and all its contents"""
    for item in os.listdir(dir_path):
        item_path: str = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)
    os.rmdir(dir_path)


def generate_test_data():
    # Get the absolute path of the current script
    current_script_dir: str = os.path.dirname(os.path.realpath(__file__))

    # Define the path to the 'data' directory
    data_dir: str = os.path.join(current_script_dir, '../data')

    # Define the path to the 'scripts/data' directory
    scripts_data_dir: str = os.path.join(current_script_dir, 'data')

    if os.path.isdir(data_dir):
        delete_directory(os.path.join(data_dir, 'movies'))
    generate_movie_files(data_dir, scripts_data_dir)

    if os.path.isdir(data_dir):
        delete_directory(os.path.join(data_dir, 'tvshows'))
    generate_tvshow_files(data_dir, scripts_data_dir)

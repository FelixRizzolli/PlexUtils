"""
This module contains functions to generate movie files based on a JSON file.
"""

import json
import os


def generate_movie_libraries(data_dir: str, scripts_data_dir: str) -> None:
    """
    Generates movie libraries based on JSON files.

    Args:
        data_dir (str): The path of the data directory where the movie files will be created.
        scripts_data_dir (str): The path of the scripts data directory where the JSON files
                                are located.
    """
    libraries = [
        {"name": "movies", "source_file": "movie_files.json"},
        {"name": "animes", "source_file": "anime_movie_files.json"},
    ]

    movies_dir = os.path.join(data_dir, "movies")
    if not os.path.isdir(movies_dir):
        os.mkdir(movies_dir)

    for lib in libraries:
        library_dir = os.path.join(movies_dir, lib["name"])
        source_file = os.path.join(scripts_data_dir, "movies", lib["source_file"])
        generate_movie_librarie(library_dir, source_file)

    print("Generate movie libraries: DONE!")


def generate_movie_librarie(library_dir: str, source_file: str) -> None:
    """
    Generates a movie library based on a JSON file.

    The function creates directories if they do not exist, then reads a JSON file containing
    movie file names. It then creates these movie files in the specified directory.

    Args:
        library_dir (str): The path of the library directory where the movie files will be created.
        source_file (str): The path of the source file where the JSON file is located.
    """
    # Open the JSON file
    print("\nRead movie_files.json")
    with open(source_file, "r", encoding="utf-8") as f:
        # Load the JSON data into a Python dictionary
        movie_files = json.load(f)["movie_files"]

    # Create library directory
    print(f"Create {library_dir} directory")
    if not os.path.isdir(library_dir):
        os.mkdir(library_dir)

    # Create movie files
    print("Create movie files")
    for movie_file in movie_files:
        with open(os.path.join(library_dir, movie_file), "a", encoding="utf-8"):
            pass

    print(f"Movie files created in '{library_dir}'.")

"""
This module contains the ScanMovieLibraryPipeline class.
"""

import json
import os
from typing import Optional

import pandas as pd
from pandas import DataFrame

from plexutils.media.video_file import VideoFile


class ScanMovieLibraryPipeline:
    """
    This class represents a pipeline for scanning a movie library.
    """

    _library_path: str
    _data_path: str
    _raw_movie_data: DataFrame

    def __init__(self, library_path: str, data_path: str):
        self._library_path = library_path
        self._data_path = data_path

    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        # Collect the file information from the movie library
        self.collect_data()

        # Load the list of movie files from a parquet file
        self.load_data()

        pass

    def collect_data(self) -> None:
        """
        This method collects the file information from the movie library and saves them to a parquet
        file.

        :return: None
        """
        movie_directories: list[str] = os.listdir(self._library_path)
        movies: list[VideoFile] = []

        # Collect file information
        for movie_dir in movie_directories:
            filepath: str = os.path.normpath(
                os.path.join(self._library_path, movie_dir)
            )
            filesize: int = os.path.getsize(filepath)
            movies.append(
                VideoFile(
                    _filepath=filepath,
                    _filesize=filesize,
                    _duration=0,
                    _resolution_width=0,
                    _resolution_height=0,
                    _video_codec="",
                    _audio_codec="",
                )
            )

        # Save the file information to a DataFrame
        movies_df: DataFrame = pd.DataFrame([movie.__dict__ for movie in movies])

        print(movies_df)

        # Save the DataFrame to a parquet file
        script_path: str = self._data_path
        file_path: str = os.path.join(script_path, "movies.parquet")
        movies_df.to_parquet(file_path, engine="pyarrow")

        pass

    def load_data(self) -> None:
        """
        This method loads the list of movie files from a parquet file into a DataFrame.

        :return: The DataFrame containing the list of movie files.
        :rtype: DataFrame
        """
        script_path: str = self._data_path
        file_path: str = os.path.join(script_path, "movies.parquet")
        movies_df: DataFrame = pd.read_parquet(file_path, engine="pyarrow")

        self._raw_movie_data = movies_df

    def project_and_save_data(self) -> None:
        """
        This method projects the list of the Movie objects & invalid files and saves them to a
        parquet file.

        :return: None
        """
        pass


if __name__ == "__main__":

    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    movie_lib = os.path.join(pj_path, "data", "movies", "movies")
    data_path = os.path.join(pj_path, "data", "raw")

    pipeline = ScanMovieLibraryPipeline(
        os.path.normpath(movie_lib), os.path.normpath(data_path)
    )
    pipeline.run()

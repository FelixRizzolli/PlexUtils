"""
This module contains the ScanMovieLibraryPipeline class.
"""

import os
from datetime import datetime
from typing import Optional
from enum import Enum

import pandas as pd
from pandas import DataFrame

from media_tools import (
    extract_tvdbid,
    get_video_codec,
    get_audio_codec,
    get_duration,
    get_resolution,
    get_format_name,
    get_bitrate,
    get_frame_rate,
    get_number_of_streams,
    get_pixel_format,
)
from mongodb import get_collection
from pipelines.base_pipeline import BaseConfig, BasePipeline
from plexutils.media.video_file import VideoFile


class MovieErrorCode(Enum):
    INVALID_TVDB_ID = "INVALID_TVDB_ID"
    INVALID_FILESIZE = "INVALID_FILESIZE"


class ScanMovieLibraryConfig(BaseConfig):
    """
    This class represents the configuration for the ScanMovieLibraryPipeline.
    """


class ScanMovieLibraryPipeline(BasePipeline):
    """
    This class represents a pipeline for scanning a movie library.
    """

    _raw_movie_data: Optional[DataFrame] = None
    _invalid_movie_data: Optional[DataFrame] = None
    _valid_movie_data: Optional[DataFrame] = None

    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        # Collect the file information from the movie library
        self.collect_data()

        # Load the list of movie files from a parquet file
        self.load_data()

        # Validate the list of movie files
        self.validate_data()

        # Project data
        self.project_data()

        # Save the invalid movie files to a MongoDB database
        self.save_invalid_movies_to_mongodb()

    def collect_data(self) -> None:
        """
        This method collects the file information from the movie library and saves them to a parquet
        file.

        :return: None
        """
        movie_directories: list[str] = os.listdir(self.config.library_path)
        movies: list[VideoFile] = []

        # Collect file information
        for movie_dir in movie_directories:
            filepath: str = os.path.normpath(
                os.path.join(self.config.library_path, movie_dir)
            )
            format_name: str = get_format_name(filepath)
            filesize: int = os.path.getsize(filepath)
            video_codec: str = get_video_codec(filepath)
            audio_codec: str = get_audio_codec(filepath)
            duration: float = get_duration(filepath)
            [resolution_width, resolution_height] = get_resolution(filepath)
            bitrate: int = get_bitrate(filepath)
            frame_rate: int = get_frame_rate(filepath)
            number_of_frames: int = get_number_of_streams(filepath)
            pixel_format: str = get_pixel_format(filepath)

            movies.append(
                VideoFile(
                    _filepath=filepath,
                    _format_name=format_name,
                    _filesize=filesize,
                    _duration=duration,
                    _resolution_width=resolution_width,
                    _resolution_height=resolution_height,
                    _video_codec=video_codec,
                    _audio_codec=audio_codec,
                    _bitrate=bitrate,
                    _frame_rate=frame_rate,
                    _number_of_streams=number_of_frames,
                    _pixel_format=pixel_format,
                )
            )

        # Save the file information to a DataFrame
        movies_df: DataFrame = pd.DataFrame([movie.__dict__ for movie in movies])

        print(movies_df)

        # Save the DataFrame to a parquet file
        script_path: str = self.config.data_path
        file_path: str = os.path.join(script_path, "movies.parquet")
        movies_df.to_parquet(file_path, engine="pyarrow")

        pass

    def load_data(self) -> None:
        """
        This method loads the list of movie files from a parquet file into a DataFrame.

        :return: The DataFrame containing the list of movie files.
        :rtype: DataFrame
        """
        script_path: str = self.config.data_path
        file_path: str = os.path.join(script_path, "movies.parquet")
        movies_df: DataFrame = pd.read_parquet(file_path, engine="pyarrow")

        self._raw_movie_data = movies_df

    def validate_data(self) -> None:
        """
        This method validates the list of movie files and removes any invalid files.

        :return: None
        """

        # Initialize _invalid_movie_data with the same structure as _raw_movie_data
        self._invalid_movie_data = pd.DataFrame(columns=self._raw_movie_data.columns)
        self._invalid_movie_data["errorcode"] = None
        invalid_rows = []

        # Initialize _valid_movie_data with the same structure as _raw_movie_data
        self._valid_movie_data = pd.DataFrame(columns=self._raw_movie_data.columns)
        valid_rows = []

        # Validate the list of movie files
        for index, row in self._raw_movie_data.iterrows():
            # Extract the TVDB ID from the filename and check if it is valid
            tvdb_id: Optional[int] = extract_tvdbid(row["filename"])
            if tvdb_id is None:
                err = MovieErrorCode.INVALID_TVDB_ID.value
                row["errorcode"] = err
                invalid_rows.append(row)
                print(f"Invalid movie file: [{err}] [{index}] {row['filename']}")

            # Check if the filesize is valid
            elif row["filesize"] <= 0:
                err = MovieErrorCode.INVALID_FILESIZE.value
                row["errorcode"] = err
                invalid_rows.append(row)
                print(f"Invalid movie file: [{err}] [{index}] {row['filename']}")

            # Valid row
            else:
                valid_rows.append(row)

        # Concatenate invalid rows to _invalid_movie_data
        if invalid_rows:
            self._invalid_movie_data = pd.concat(
                [self._invalid_movie_data, pd.DataFrame(invalid_rows)],
                ignore_index=True,
            ).dropna(how="all", axis=1)

        # Concatenate valid rows to _valid_movie_data
        if valid_rows:
            self._valid_movie_data = pd.concat(
                [self._valid_movie_data, pd.DataFrame(valid_rows)],
                ignore_index=True,
            ).dropna(how="all", axis=1)

    def project_data(self) -> None:
        """
        This method projects the valid movie files to a new DataFrame.

        :return: None
        """

        # Add the processing date column with the current timestamp
        if self._invalid_movie_data is not None:
            self._invalid_movie_data["processing_date"] = datetime.now()

        # Add the processing date column with the current timestamp
        if self._valid_movie_data is not None:
            self._valid_movie_data["processing_date"] = datetime.now()

    def save_invalid_movies_to_mongodb(self) -> None:
        """
        This method saves the invalid movie files to a MongoDB database.

        :return: None
        """
        if self._invalid_movie_data is not None and len(self._invalid_movie_data) > 0:
            invalid_movies_collection = get_collection("raw_data", "invalid_movies")
            invalid_movies_collection.insert_many(
                self._invalid_movie_data.to_dict("records")
            )

            runs_collection = get_collection("sys", "runs")
            runs_collection.insert_one(
                {
                    "database": "raw_data",
                    "collection": "invalid_movies",
                    "library": self.config.library_name,
                    "application": "plexutils",
                    "type": "library-scan",
                    "processing_date": datetime.now(),
                }
            )

        if self._valid_movie_data is not None and len(self._valid_movie_data) > 0:
            movies_collection = get_collection("raw_data", "movies")
            movies_collection.insert_many(self._valid_movie_data.to_dict("records"))

            runs_collection = get_collection("sys", "runs")
            runs_collection.insert_one(
                {
                    "database": "raw_data",
                    "collection": "movies",
                    "library": self.config.library_name,
                    "application": "plexutils",
                    "type": "library-scan",
                    "processing_date": datetime.now(),
                }
            )


if __name__ == "__main__":
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    movie_lib = os.path.join(pj_path, "data", "movies", "animes")
    data_path = os.path.join(pj_path, "data", "raw")

    pipeline = ScanMovieLibraryPipeline()
    pipeline.config = ScanMovieLibraryConfig(
        library_name="movies",
        library_path=os.path.normpath(movie_lib),
        data_path=os.path.normpath(data_path),
    )
    pipeline.run()

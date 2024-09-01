"""
This module contains the ScanMovieLibraryPipeline class.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional, List
from enum import Enum

import pandas as pd
from pandas import DataFrame
from loguru import logger

from plexutils.shared.mongodb_tools import get_collection
from plexutils.shared.media_tools import extract_tvdbid, collect_video_file_data
from plexutils.pipelines.base_pipeline import is_empty
from plexutils.pipelines.base_pipeline import (
    BaseLibraryConfig,
    BasePipeline,
    pipeline_runner,
    is_not_empty,
)
from plexutils.media.video_file import VideoFile


class MovieErrorCode(Enum):
    INVALID_TVDB_ID = "INVALID_TVDB_ID"
    INVALID_FILESIZE = "INVALID_FILESIZE"


class ScanMovieLibraryConfig(BaseLibraryConfig):
    """
    This class represents the configuration for the ScanMovieLibraryPipeline.
    """


class ScanMovieLibraryPipeline(BasePipeline):
    """
    This class represents a pipeline for scanning a movie library.
    """

    _config: Optional[ScanMovieLibraryConfig] = None
    _raw_movie_data: Optional[DataFrame] = None
    _invalid_movie_data: Optional[DataFrame] = None
    _valid_movie_data: Optional[DataFrame] = None

    def __init__(self, config: Optional[ScanMovieLibraryConfig] = None):
        self._config = config

    @pipeline_runner
    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        # Set the execution start time.
        self.config.execution_start_time = datetime.now()

        # Collect the file information from the movie library
        self.collect_data()
        if is_empty(self.raw_movie_data):
            logger.error("No movie files found in the library.")
            return
        logger.info(f"Total Movies: {len(self._raw_movie_data)}")

        # Save the movie file data to a parquet file
        self.save_data()
        logger.info("Saved movie files successfully to parquet.")

        # Validate the list of movie files
        self.validate_data()
        if is_not_empty(self.invalid_movie_data):
            logger.error(f"Invalid Movies...: {len(self.invalid_movie_data)}")
        if is_not_empty(self.valid_movie_data):
            logger.info(f"Valid Movies.....: {len(self.valid_movie_data)}")

        # Project data
        self.project_data()
        logger.info("Data projected successfully.")

        # Save the invalid movie files to a MongoDB database
        if is_not_empty(self.invalid_movie_data):
            self.save_invalid_movies_to_mongodb()
            logger.info("Invalid movies saved to MongoDB.")

        if is_not_empty(self.valid_movie_data):
            self.save_valid_movies_to_mongodb()
            logger.info("Valid movies saved to MongoDB.")

        # Set the execution end time.
        self.config.execution_end_time = datetime.now()

        # Save the run information to a MongoDB database.
        self.save_run_information_to_mongodb()

    @property
    def config(self) -> ScanMovieLibraryConfig:
        """
        Returns the configuration for the pipeline.

        :return: The configuration for the pipeline.
        :rtype: ScanMovieLibraryConfig
        """
        return self._config

    @property
    def raw_movie_data(self) -> Optional[DataFrame]:
        """
        Returns the raw movie data.

        :return: The raw movie data.
        :rtype: Optional[DataFrame]
        """
        return self._raw_movie_data

    @property
    def invalid_movie_data(self) -> Optional[DataFrame]:
        """
        Returns the invalid movie data.

        :return: The invalid movie data.
        :rtype: Optional[DataFrame]
        """
        return self._invalid_movie_data

    @property
    def valid_movie_data(self) -> Optional[DataFrame]:
        """
        Returns the valid movie data.

        :return: The valid movie data.
        :rtype: Optional[DataFrame]
        """
        return self._valid_movie_data

    def collect_data(self) -> None:
        """
        This method collects the file information from the movie library and saves them to a parquet
        file.

        :return: None
        """
        # Get the list of movie directories
        movie_directories: list[str] = os.listdir(self.config.library_path)

        # Collect file information from the movie library
        movies: list[VideoFile] = self.collect_data_parallel(movie_directories)

        # Save the file information to a DataFrame
        self._raw_movie_data = pd.DataFrame([movie.__dict__ for movie in movies])

    def collect_data_parallel(self, movie_directories: List[str]) -> List[VideoFile]:
        """
        This method collects the data for multiple movie files in parallel.

        :param movie_directories: The list of movie directories.
        :return: The list of movie files.
        """
        movies: list[VideoFile] = []

        with ThreadPoolExecutor() as executor:
            future_to_movie = {
                executor.submit(
                    collect_video_file_data, self.config.library_path, movie_dir
                ): movie_dir
                for movie_dir in movie_directories
            }

            for future in as_completed(future_to_movie):
                movie_dir = future_to_movie[future]
                try:
                    video_file: VideoFile = future.result()
                    movies.append(video_file)
                except Exception as exc:
                    logger.error(f"{movie_dir} generated an exception: {exc}")

        return movies

    def save_data(self) -> None:
        """
        This method saves the list of movie files to a parquet file.

        :return: None
        """
        parquet_name: str = self.config.library_name + "_movies.parquet"
        file_path: str = os.path.join(self.config.data_path, parquet_name)
        self._raw_movie_data.to_parquet(file_path, engine="pyarrow")

    def load_data(self) -> None:
        """
        This method loads the list of movie files from a parquet file into a DataFrame.

        :return: The DataFrame containing the list of movie files.
        :rtype: DataFrame
        """
        parquet_name: str = self.config.library_name + "_movies.parquet"
        file_path: str = os.path.join(self.config.data_path, parquet_name)
        movies_df: DataFrame = pd.read_parquet(file_path, engine="pyarrow")

        self._raw_movie_data = movies_df

    def validate_data(self) -> None:
        """
        This method validates the list of movie files and removes any invalid files.

        :return: None
        """
        if self.raw_movie_data is None:
            return

        # Initialize _invalid_movie_data with the same structure as _raw_movie_data
        self._invalid_movie_data = pd.DataFrame(columns=self._raw_movie_data.columns)
        self._invalid_movie_data["errorCode"] = None
        invalid_rows = []

        # Initialize _valid_movie_data with the same structure as _raw_movie_data
        self._valid_movie_data = pd.DataFrame(columns=self._raw_movie_data.columns)
        valid_rows = []

        # Validate the list of movie files
        for index, row in self._raw_movie_data.iterrows():
            # Extract the TVDB ID from the filename and check if it is valid
            tvdb_id: Optional[int] = extract_tvdbid(row["file"]["name"])
            if tvdb_id is None:
                err: str = MovieErrorCode.INVALID_TVDB_ID.value
                row["errorCode"] = err
                invalid_rows.append(row)
                logger.error(
                    f"Invalid movie file: [{err}] [{index}] {row['file']['name']}"
                )

            # Check if the filesize is valid
            elif row["file"]["size"] <= 0:
                err: str = MovieErrorCode.INVALID_FILESIZE.value
                row["errorCode"] = err
                invalid_rows.append(row)
                logger.error(
                    f"Invalid movie file: [{err}] [{index}] {row['file']['name']}"
                )

            # Valid movie file
            else:
                valid_rows.append(row)

        # Concatenate invalid rows to _invalid_movie_data
        if len(invalid_rows) > 0:
            if is_empty(self.invalid_movie_data):
                self._invalid_movie_data = pd.DataFrame(invalid_rows)
            else:
                self._invalid_movie_data = pd.concat(
                    [self._invalid_movie_data, pd.DataFrame(invalid_rows)],
                    ignore_index=True,
                ).dropna(how="all", axis=1)
        else:
            self._invalid_movie_data = pd.DataFrame([])

        # Concatenate valid rows to _valid_movie_data
        if len(valid_rows) > 0:
            if is_empty(self.valid_movie_data):
                self._valid_movie_data = pd.DataFrame(valid_rows)
            else:
                self._valid_movie_data = pd.concat(
                    [self._valid_movie_data, pd.DataFrame(valid_rows)],
                    ignore_index=True,
                ).dropna(how="all", axis=1)
        else:
            self._valid_movie_data = pd.DataFrame([])

    def project_data(self) -> None:
        """
        This method projects the valid movie files to a new DataFrame.

        :return: None
        """
        # Add the processing date column with the current timestamp
        if is_not_empty(self.invalid_movie_data):
            self._invalid_movie_data["processing_date"] = datetime.now()

        # Add the processing date column with the current timestamp
        if is_not_empty(self.valid_movie_data):
            self._valid_movie_data["processing_date"] = datetime.now()

    def save_invalid_movies_to_mongodb(self) -> None:
        """
        This method saves the invalid movie files to a MongoDB database.

        :return: None
        """
        invalid_movies_collection = get_collection("raw_data", "invalid_movies")
        invalid_movies_collection.insert_many(
            self.invalid_movie_data.to_dict("records")
        )

    def save_valid_movies_to_mongodb(self) -> None:
        """
        This method saves the valid movie files to a MongoDB database.

        :return: None
        """
        movies_collection = get_collection("raw_data", "movies")
        movies_collection.insert_many(self.valid_movie_data.to_dict("records"))

    def save_run_information_to_mongodb(self) -> None:
        """
        This method saves the run information to a MongoDB database.

        :return: None
        """
        base_run_information = {
            "database": "raw_data",
            "libearyType": "movie",
            "libraryName": self.config.library_name,
            "application": "plexutils",
            "type": "library-scan",
            "executionStartTime": self.config.execution_start_time,
            "executionEndTime": self.config.execution_end_time,
        }

        if is_not_empty(self.invalid_movie_data):
            invalid_movies_collection = get_collection("sys", "runs")
            invalid_movies_collection.insert_one(
                {**base_run_information, "collection": "invalid_movies"}
            )

        if is_not_empty(self.valid_movie_data):
            movies_collection = get_collection("sys", "runs")
            movies_collection.insert_one(
                {**base_run_information, "collection": "movies"}
            )


if __name__ == "__main__":
    library_name: str = "[DE-XX] Movies"

    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    movie_lib = os.path.join(pj_path, "data", "movies", "animes")
    data_path = os.path.join(pj_path, "data", "raw")

    # library_path = os.path.normpath(movie_lib)
    library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"

    pipeline_config = ScanMovieLibraryConfig(
        library_name=library_name,
        library_path=library_path,
        data_path=os.path.normpath(data_path),
    )
    pipeline = ScanMovieLibraryPipeline(pipeline_config)
    pipeline.run()

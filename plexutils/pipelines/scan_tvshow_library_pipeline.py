import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from enum import Enum
from typing import Optional, List

import pandas as pd
from loguru import logger
from pandas import DataFrame

from base_pipeline import (
    BaseLibraryConfig,
    BasePipeline,
    pipeline_runner,
    is_not_empty,
    is_empty,
)
from mongodb import get_collection
from video_file import VideoFile
from media_tools import extract_tvdbid, collect_video_file_data


class TVShowErrorCode(Enum):
    INVALID_TVDB_ID = "INVALID_TVDB_ID"
    INVALID_FILESIZE = "INVALID_FILESIZE"


class ScanTvShowLibraryConfig(BaseLibraryConfig):
    """
    This class represents the configuration for the ScanTvShowLibraryPipeline.
    """


class ScanTvShowLibraryPipeline(BasePipeline):
    """
    This class represents a pipeline for scanning a TV show library.
    """

    _config: Optional[ScanTvShowLibraryConfig] = None
    _raw_tvshow_data: Optional[DataFrame] = None

    _invalid_episode_files: Optional[DataFrame] = None
    _valid_episode_files: Optional[DataFrame] = None

    def __init__(self, config: ScanTvShowLibraryConfig):
        self._config = config

    @pipeline_runner
    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        # Set the execution start time.
        self.config.execution_start_time = datetime.now()

        # Collect the file information from the tv show library.
        self.collect_data()
        if is_empty(self.raw_tvshow_data):
            logger.error("No TV Shows found.")
            return

        # Save the tv show file data to a parquet file.
        self.save_data()

        # Validate the list of tv show files.
        self.validate_data()
        if is_not_empty(self.valid_episode_files):
            logger.info(f"Valid Episodes: {len(self.valid_episode_files)}")
        if is_not_empty(self.invalid_episode_files):
            logger.info(f"Invalid Episodes: {len(self.invalid_episode_files)}")

        # Project data
        self.project_data()

        # Save the invalid tv show files to a MongoDB database.
        if is_not_empty(self.invalid_episode_files):
            self.save_invalid_episode_files_to_mongodb()

        # Save the valid tv show files to a MongoDB database.
        if is_not_empty(self.valid_episode_files):
            self.save_valid_episode_files_to_mongodb()

        # Set the execution end time.
        self.config.execution_end_time = datetime.now()

        # Save the run information to a MongoDB database.
        self.save_run_information_to_mongodb()

    @property
    def config(self) -> ScanTvShowLibraryConfig:
        """
        Returns the configuration.

        :return: The configuration.
        :rtype: ScanTvShowLibraryConfig
        """
        return self._config

    @property
    def raw_tvshow_data(self) -> DataFrame:
        """
        Returns the raw TV show data.

        :return: The raw TV show data.
        :rtype: DataFrame
        """
        return self._raw_tvshow_data

    @property
    def invalid_episode_files(self) -> DataFrame:
        """
        Returns the invalid episode files.

        :return: The invalid episode files.
        :rtype: DataFrame
        """
        return self._invalid_episode_files

    @property
    def valid_episode_files(self) -> DataFrame:
        """
        Returns the valid episode files.

        :return: The valid episode files.
        :rtype: DataFrame
        """
        return self._valid_episode_files

    def collect_data(self) -> None:
        """
        Collects the data.

        :return: None
        """
        tvshows_df: DataFrame = self.collect_tvshow_data()

        seasons_df: DataFrame = None
        for _, tvshow_df in tvshows_df.iterrows():
            new_seasons: DataFrame = self.collect_season_data(
                tvshow_df["tvshow"], tvshow_df["path"]
            )
            if seasons_df is None:
                seasons_df = new_seasons
            else:
                seasons_df = pd.concat([seasons_df, new_seasons])

        episodes_df: DataFrame = None
        for _, season_df in seasons_df.iterrows():
            new_episodes: DataFrame = self.collect_episode_data(
                season_df["tvshow"], season_df["season"], season_df["path"]
            )
            if episodes_df is None:
                episodes_df = new_episodes
            else:
                episodes_df = pd.concat([episodes_df, new_episodes])

        if is_empty(tvshows_df):
            logger.error("No TV Shows found.")
        else:
            logger.info(f"Total TV Shows: {len(tvshows_df)}")

        if is_empty(seasons_df):
            logger.error("No Seasons found.")
        else:
            logger.info(f"Total Seasons: {len(seasons_df)}")

        if is_empty(episodes_df):
            logger.error("No Episodes found.")
        else:
            logger.info(f"Total Episodes: {len(episodes_df)}")

        self._raw_tvshow_data = episodes_df
        print(self._raw_tvshow_data)

    def collect_tvshow_data(self) -> DataFrame:
        """
        Collects the TV show data.

        :return: None
        """
        tvshows: list[str] = os.listdir(self.config.library_path)
        tvshow_data = []

        for tvshow in tvshows:
            tvshow_path = os.path.join(self.config.library_path, tvshow)
            if os.path.isdir(tvshow_path):
                tvshow_data.append({"tvshow": tvshow, "path": tvshow_path})

        return pd.DataFrame(tvshow_data)

    def collect_season_data(self, tvshow_name: str, tvshow_path: str) -> DataFrame:
        """
        Collects the season data.

        :return: None
        """
        seasons: list[str] = os.listdir(tvshow_path)
        season_data = []

        for season in seasons:
            season_path = os.path.join(tvshow_path, season)
            if os.path.isdir(season_path):
                season_data.append(
                    {"tvshow": tvshow_name, "season": season, "path": season_path}
                )

        return pd.DataFrame(season_data)

    def collect_episode_data(
        self, tvshow_name: str, season_name: str, season_path: str
    ) -> DataFrame:
        """
        Collects the episode data.

        :return: None
        """
        # Get the list of episodes in the season directory.
        episodes: list[str] = os.listdir(season_path)

        # Collect the file information from the tv show library.
        episode_data = self.collect_data_parallel(
            tvshow_name, season_name, season_path, episodes
        )

        # Return the episode data as a DataFrame
        return pd.DataFrame([episode for episode in episode_data])

    def collect_data_parallel(
        self,
        tvshow_name: str,
        season_name: str,
        season_path: str,
        episode_directories: List[str],
    ) -> List[VideoFile]:
        episodes: list[VideoFile] = []

        with ThreadPoolExecutor() as executor:
            future_to_episode = {
                executor.submit(
                    collect_video_file_data,
                    self.config.library_path,
                    os.path.join(season_path, episode_dir),
                ): episode_dir
                for episode_dir in episode_directories
            }

            for future in as_completed(future_to_episode):
                episode_dir = future_to_episode[future]
                try:
                    path_data: dict = {
                        "tvshow": tvshow_name,
                        "season": season_name,
                    }
                    video_file: VideoFile = future.result()
                    video_data = video_file.__dict__
                    episodes.append({**path_data, **video_data})
                except Exception as exc:
                    print(f"{episode_dir} generated an exception: {exc}")

        return episodes

    def save_data(self) -> None:
        """
        This method saves the list of movie files to a parquet file.

        :return: None
        """
        parquet_name: str = self.config.library_name + "_tvshows.parquet"
        file_path: str = os.path.join(self.config.data_path, parquet_name)

        if self.raw_tvshow_data is not None and isinstance(
            self.raw_tvshow_data, DataFrame
        ):
            self._raw_tvshow_data.to_parquet(file_path, engine="pyarrow")

    def load_data(self) -> None:
        """
        This method loads the list of movie files from a parquet file into a DataFrame.

        :return: The DataFrame containing the list of movie files.
        :rtype: DataFrame
        """
        parquet_name: str = self.config.library_name + "_tvshows.parquet"
        file_path: str = os.path.join(self.config.data_path, parquet_name)
        tvshows_df: DataFrame = pd.read_parquet(file_path, engine="pyarrow")

        self._raw_tvshow_data = tvshows_df

    def validate_data(self) -> None:
        """
        This method validates the list of movie files.

        :return: None
        """
        if self.raw_tvshow_data is None:
            return

        # Initialize _invalid_episode_files with the same structure as _raw_tvshow_data
        self._invalid_episode_files = pd.DataFrame(
            columns=self._raw_tvshow_data.columns
        )
        self._invalid_episode_files["errorCode"] = None
        invalid_rows = []

        # Initialize _valid_episode_files with the same structure as _raw_tvshow_data
        self._valid_episode_files = pd.DataFrame(columns=self._raw_tvshow_data.columns)
        valid_rows = []

        # Validate the list of episode files.
        for index, row in self._raw_tvshow_data.iterrows():
            # Extract the TVDB ID from the episode file name and check if it is valid.
            tvdb_id: Optional[int] = extract_tvdbid(row["tvshow"])
            if tvdb_id is None:
                err: str = TVShowErrorCode.INVALID_TVDB_ID.value
                row["errorCode"] = err
                invalid_rows.append(row)
                print(f"Invalid episode file: [{err}] [{index}] {row['file']['name']}")

            # Check if the file size is valid.
            elif row["file"]["size"] <= 0:
                err: str = TVShowErrorCode.INVALID_FILESIZE.value
                row["errorCode"] = err
                invalid_rows.append(row)
                print(f"Invalid episode file: [{err}] [{index}] {row['file']['name']}")

            # Valid episode file
            else:
                valid_rows.append(row)

        # Concatenate invalid rows to _invalid_episode_files
        if len(invalid_rows) > 0:
            if is_empty(self.invalid_episode_files):
                self._invalid_episode_files = pd.DataFrame(invalid_rows)
            else:
                self._invalid_episode_files = pd.concat(
                    [self._invalid_episode_files, pd.DataFrame(invalid_rows)],
                    ignore_index=True,
                ).dropna(how="all", axis=1)
        else:
            self._invalid_episode_files = pd.DataFrame([])

        # Concatenate valid rows to _valid_episode_files
        if len(valid_rows) > 0:
            if is_empty(self.valid_episode_files):
                self._valid_episode_files = pd.DataFrame(valid_rows)
            else:
                self._valid_episode_files = pd.concat(
                    [self._valid_episode_files, pd.DataFrame(valid_rows)],
                    ignore_index=True,
                ).dropna(how="all", axis=1)
        else:
            self._valid_episode_files = pd.DataFrame([])

    def project_data(self) -> None:
        """
        This method projects the data.

        :return: None
        """
        # Add the processing date column with the current timestamp
        if is_not_empty(self.invalid_episode_files):
            self._invalid_episode_files["processing_date"] = datetime.now()

        # Add the processing date column with the current timestamp
        if is_not_empty(self.valid_episode_files):
            self._valid_episode_files["processing_date"] = datetime.now()

    def save_invalid_episode_files_to_mongodb(self) -> None:
        """
        This method saves the invalid episode files to a MongoDB database.

        :return: None
        """
        invalid_episodes_collection = get_collection("raw_data", "invalid_episodes")
        invalid_episodes_collection.insert_many(
            self.invalid_episode_files.to_dict("records")
        )

    def save_valid_episode_files_to_mongodb(self) -> None:
        """
        This method saves the valid episode files to a MongoDB database.

        :return: None
        """
        episodes_collection = get_collection("raw_data", "episodes")
        episodes_collection.insert_many(self.valid_episode_files.to_dict("records"))

    def save_run_information_to_mongodb(self) -> None:
        """
        This method saves the run information to a MongoDB database.

        :return: None
        """
        base_run_information = {
            "database": "raw_data",
            "libearyType": "tvshow",
            "libraryName": self.config.library_name,
            "application": "plexutils",
            "type": "library-scan",
            "executionStartTime": self.config.execution_start_time,
            "executionEndTime": self.config.execution_end_time,
        }

        if is_not_empty(self.invalid_episode_files):
            invalid_episodes_collection = get_collection("sys", "runs")
            invalid_episodes_collection.insert_one(
                {**base_run_information, "collection": "invalid_episodes"}
            )

        if is_not_empty(self.valid_episode_files):
            episodes_collection = get_collection("sys", "runs")
            episodes_collection.insert_one(
                {**base_run_information, "collection": "episodes"}
            )


if __name__ == "__main__":
    library_name: str = "[DE-XX] Serien"

    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    tvshows_lib = os.path.join(pj_path, "data", "tvshows", "animes")
    data_path = os.path.join(pj_path, "data", "raw")

    # library_path = os.path.normpath(tvshows_lib)
    library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"

    pipeline_config = ScanTvShowLibraryConfig(
        library_name=library_name,
        library_path=library_path,
        data_path=os.path.normpath(data_path),
    )
    pipeline = ScanTvShowLibraryPipeline(pipeline_config)
    pipeline.run()

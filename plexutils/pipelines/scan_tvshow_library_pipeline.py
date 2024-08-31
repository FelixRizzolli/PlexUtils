import os
from datetime import datetime
from enum import Enum
from typing import Optional

import pandas as pd
from loguru import logger
from pandas import DataFrame

from base_pipeline import BaseLibraryConfig, BasePipeline, pipeline_runner
from mongodb import get_collection
from video_file import VideoFile
from media_tools import extract_tvdbid


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

        # Collect the file information from the tv show library.
        self.collect_data()

        # Save the tv show file data to a parquet file.
        self.save_data()

        # Validate the list of tv show files.
        self.validate_data()
        if self.valid_episode_files is not None:
            logger.info(f"Valid Episodes: {len(self.valid_episode_files)}")
        if self.invalid_episode_files is not None:
            logger.info(f"Invalid Episodes: {len(self.invalid_episode_files)}")

        # Project data
        self.project_data()

        # Save the invalid tv show files to a MongoDB database.
        if (
            self.invalid_episode_files is not None
            and not self.invalid_episode_files.empty
        ):
            self.save_invalid_episode_files_to_mongodb()

        # Save the valid tv show files to a MongoDB database.
        if self.valid_episode_files is not None and not self.valid_episode_files.empty:
            self.save_valid_episode_files_to_mongodb()

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

        if tvshow_df is None or tvshow_df.empty:
            logger.error("No TV Shows found.")
        else:
            logger.info(f"Total TV Shows: {len(tvshows_df)}")

        if seasons_df is None or seasons_df.empty:
            logger.error("No Seasons found.")
        else:
            logger.info(f"Total Seasons: {len(seasons_df)}")

        if episodes_df is None or episodes_df.empty:
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
        episodes: list[str] = os.listdir(season_path)
        episode_data = []

        for episode in episodes:
            episode_path = os.path.join(season_path, episode)
            if os.path.isfile(episode_path):
                path_data: dict = {
                    "tvshow": tvshow_name,
                    "season": season_name,
                    "episode": episode,
                    "path": episode_path,
                }
                video_file: VideoFile = VideoFile(episode_path)
                video_file.collect_data()
                video_data = video_file.__dict__
                episode_data.append({**path_data, **video_data})

        return pd.DataFrame([episode for episode in episode_data])

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
        self._invalid_episode_files["error_code"] = None
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
                row["error_code"] = err
                invalid_rows.append(row)
                print(f"Invalid episode file: [{err}] [{index}] {row['file_name']}")

            # Check if the file size is valid.
            elif row["file_size"] <= 0:
                err: str = TVShowErrorCode.INVALID_FILESIZE.value
                row["error_code"] = err
                invalid_rows.append(row)
                print(f"Invalid episode file: [{err}] [{index}] {row['file_name']}")

            # Valid episode file
            else:
                valid_rows.append(row)

        # Concatenate invalid rows to _invalid_episode_files
        if len(invalid_rows) > 0:
            if self.invalid_episode_files is None or self.invalid_episode_files.empty:
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
            if self.valid_episode_files is None or self.valid_episode_files.empty:
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
        if (
            self.invalid_episode_files is not None
            and not self.invalid_episode_files.empty
        ):
            self._invalid_episode_files["processing_date"] = datetime.now()

        # Add the processing date column with the current timestamp
        if self.valid_episode_files is not None and not self.valid_episode_files.empty:
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

        runs_collection = get_collection("sys", "runs")
        runs_collection.insert_one(
            {
                "database": "raw_data",
                "collection": "invalid_episodes",
                "library": self.config.library_name,
                "application": "plexutils",
                "type": "library-scan",
                "processing_date": datetime.now(),
            }
        )

    def save_valid_episode_files_to_mongodb(self) -> None:
        """
        This method saves the valid episode files to a MongoDB database.

        :return: None
        """
        episodes_collection = get_collection("raw_data", "episodes")
        episodes_collection.insert_many(self.valid_episode_files.to_dict("records"))

        runs_collection = get_collection("sys", "runs")
        runs_collection.insert_one(
            {
                "database": "raw_data",
                "collection": "episodes",
                "library": self.config.library_name,
                "application": "plexutils",
                "type": "library-scan",
                "processing_date": datetime.now(),
            }
        )


if __name__ == "__main__":
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    tvshows_lib = os.path.join(pj_path, "data", "tvshows", "animes")
    data_path = os.path.join(pj_path, "data", "raw")

    library_path = os.path.normpath(tvshows_lib)
    # library_path = "/Volumes/PlexLibrary/TVShows/[EN-XX] Animationsserien"

    pipeline_config = ScanTvShowLibraryConfig(
        library_name="tvshows",
        library_path=library_path,
        data_path=os.path.normpath(data_path),
    )
    pipeline = ScanTvShowLibraryPipeline(pipeline_config)
    pipeline.run()

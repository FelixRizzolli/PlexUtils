import os
from typing import Optional

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from loguru import logger

from base_pipeline import BaseLibraryConfig, BasePipeline, pipeline_runner
from video_file import VideoFile


class ScanTvShowLibraryConfig(BaseLibraryConfig):
    """
    This class represents the configuration for the ScanTvShowLibraryPipeline.
    """


class ScanTvShowLibraryPipeline(BasePipeline):
    """
    This class represents a pipeline for scanning a TV show library.
    """

    _config: Optional[ScanTvShowLibraryConfig] = None
    _tvshow_data: Optional[DataFrame] = None

    def __init__(self, config: ScanTvShowLibraryConfig):
        self._config = config

    @pipeline_runner
    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        # Collect the data.
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

        logger.info(f"Total TV Shows: {len(tvshows_df)}")
        logger.info(f"Total Seasons: {len(seasons_df)}")
        logger.info(f"Total Episodes: {len(episodes_df)}")

        pass

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

        return pd.DataFrame(episode_data)


if __name__ == "__main__":
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    movie_lib = os.path.join(pj_path, "data", "movies", "animes")
    data_path = os.path.join(pj_path, "data", "raw")

    # library_path = os.path.normpath(movie_lib)
    library_path = "/Volumes/PlexLibrary/TVShows/[EN-XX] Animationsserien"

    pipeline_config = ScanTvShowLibraryConfig(
        library_name="tvshows",
        library_path=library_path,
        data_path=os.path.normpath(data_path),
    )
    pipeline = ScanTvShowLibraryPipeline(pipeline_config)
    pipeline.run()

"""
    This module contains TVShowSeason class.
"""
from typing import Optional, List

from plexutils.shared.utils import extract_seasonid
from plexutils.media.tvshow_episode import TVShowEpisode


class TVShowSeason:
    """represents a single season of a tv show"""
    def __init__(self, dirname):
        self.season_id: Optional[int] = extract_seasonid(dirname)
        self.dirname: str = dirname
        self.episodes: List[TVShowEpisode] = []

    def get_id(self) -> Optional[int]:
        """returns the season id"""
        return self.season_id

    def is_valid(self) -> bool:
        """checks if the seasons directory name is valid"""
        return self.season_id is not None

    def get_episodes(self) -> List[TVShowEpisode]:
        """returns all the episodes of the season"""
        return self.episodes

    def get_episodeids(self) -> List[int]:
        """returns all the episode ids of the season"""
        ids: List[int] = []
        for episode in self.episodes:
            ids.append(episode.get_id())
        return ids

    def add_episode(self, episode: TVShowEpisode) -> None:
        """adds an episode to the season"""
        self.episodes.append(episode)

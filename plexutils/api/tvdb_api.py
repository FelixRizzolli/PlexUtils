"""
    This module contains TvdbApi class.
"""

import ssl
from typing import Optional

from tvdb_v4_official import TVDB

from plexutils.shared.date_tools import is_past_date

# pylint: disable=protected-access
ssl._create_default_https_context = ssl._create_unverified_context


class TvdbApi:
    """class for accessing the tvdb api"""

    def __init__(self, key: str, pin: str):
        self.tvdb: TVDB = TVDB(key, pin)
        self.cached_episodes: list[dict] = []
        self.cached_tvshow_tvdbid: Optional[int] = None

    def get_movie(self, movie_id: int) -> dict:
        """
        returns the movie data
            from the tvdb api
            for the given movie id

        :param movie_id: The movie id
        :type movie_id: int

        :return: The movie data
        :rtype: dict
        """
        return self.tvdb.get_movie(movie_id)

    def get_episodes(self, tvdbid: int, season_id: int) -> list[dict]:
        """
        returns the episodes data
            from the tvdb api
            for the given tvdbid and the season of the tvshow

        :param tvdbid: The tvdb id of the tvshow
        :type tvdbid: int
        :param season_id: The season id of the tvshow
        :type season_id: int

        :return: The episodes data
        :rtype: list[dict]
        """
        episodes: list[dict] = self.tvdb.get_series_episodes(tvdbid)["episodes"]

        clean_ep_list: list[dict] = []
        for episode in episodes:
            if episode["seasonNumber"] == season_id and episode["isMovie"] == 0:
                clean_ep: dict = {
                    "id": episode["id"],
                    "aired": episode["aired"],
                }
                clean_ep_list.append(clean_ep)

        return clean_ep_list

    def get_seasonids(self, tvdbid: int) -> set[int]:
        """
        returns the season ids
            from the tvdb api
            for the given tvdbid of the tvshow

        :param tvdbid: The tvdb id of the tvshow
        :type tvdbid: int

        :return: The season ids
        :rtype: set[int]
        """
        episodes: list[dict] = self.tvdb.get_series_episodes(tvdbid)["episodes"]

        seasonid_list: set[int] = set()
        for episode in episodes:
            if episode["seasonNumber"] != 0 and episode["isMovie"] == 0:
                season_id: int = int(episode["seasonNumber"])
                seasonid_list.add(season_id)

        return seasonid_list

    def get_episodeids(self, tvdbid: int, season_id: int) -> set[int]:
        """
        returns the season ids
            from the tvdb api
            for the given tvdbid and the season of the tvshow

        :param tvdbid: The tvdb id of the tvshow
        :type tvdbid: int
        :param season_id: The season id of the tvshow
        :type season_id: int

        :return: The season ids
        :rtype: set[int]
        """
        if self.cached_tvshow_tvdbid is None or self.cached_tvshow_tvdbid != tvdbid:
            self.cached_episodes = self.tvdb.get_series_episodes(tvdbid)["episodes"]
            self.cached_tvshow_tvdbid = tvdbid

        episodes = self.cached_episodes

        episodeid_list: set[int] = set()
        for episode in episodes:
            if (
                episode["seasonNumber"] == season_id
                and episode["isMovie"] == 0
                and is_past_date(episode["aired"])
            ):
                episode_id: int = int(episode["number"])
                episodeid_list.add(episode_id)

        return episodeid_list

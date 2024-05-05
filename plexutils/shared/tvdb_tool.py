"""
    This module contains TVDBTool class.
"""
import ssl
from tvdb_v4_official import TVDB

from plexutils.shared.utils import is_past_date

# pylint: disable=protected-access
ssl._create_default_https_context = ssl._create_unverified_context


class TVDBTool:
    """class for accessing the tvdb api"""

    def __init__(self, key, pin):
        self.tvdb = TVDB(key, pin)
        self.cached_episodes = []
        self.cached_episodes_tvdbid = None

    def get_movie(self, movie_id):
        """
            returns the movie data
                from the tvdb api
                for the given movie id
        """
        return self.tvdb.get_movie(movie_id)

    def get_episodes(self, tvdbid, season_id):
        """
            returns the episodes data
                from the tvdb api
                for the given tvdbid and the season of the tvshow
        """
        episodes = self.tvdb.get_series_episodes(tvdbid)['episodes']

        clean_ep_list = []
        for episode in episodes:
            if episode['seasonNumber'] == season_id and episode['isMovie'] == 0:
                clean_ep = {
                    'id': episode['id'],
                    'aired': episode['aired'],
                }
                clean_ep_list.append(clean_ep)

        return clean_ep_list

    def get_seasonids(self, tvdbid):
        """
            returns the season ids
                from the tvdb api
                for the given tvdbid of the tvshow
        """
        episodes = self.tvdb.get_series_episodes(tvdbid)['episodes']

        seasonid_list = set()
        for episode in episodes:
            if episode['seasonNumber'] != 0 and episode['isMovie'] == 0:
                seasonid_list.add(episode['seasonNumber'])

        return seasonid_list

    def get_episodeids(self, tvdbid, season_id):
        """
            returns the season ids
                from the tvdb api
                for the given tvdbid and the season of the tvshow
        """
        if self.cached_episodes_tvdbid is None or self.cached_episodes_tvdbid != tvdbid:
            self.cached_episodes = self.tvdb.get_series_episodes(tvdbid)['episodes']
            self.cached_episodes_tvdbid = tvdbid

        episodes = self.cached_episodes

        episodeid_list = set()
        for episode in episodes:
            if (episode['seasonNumber'] == season_id
                    and episode['isMovie'] == 0
                    and is_past_date(episode['aired'])):
                episodeid_list.add(episode['number'])

        return episodeid_list

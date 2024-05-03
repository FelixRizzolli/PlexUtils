from tvdb_v4_official import TVDB
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TVDBTool:
    def __init__(self, key, pin):
        self.tvdb = TVDB(key, pin)

    def get_movie(self, movie_id):
        return self.tvdb.get_movie(movie_id)

    def get_episodes(self, tvdb_id, season_id):
        episodes = self.tvdb.get_series_episodes(tvdb_id)["episodes"]

        clean_ep_list = []
        for episode in episodes:
            if episode["seasonNumber"] == season_id and episode["isMovie"] == 0:
                clean_ep = {
                    "id": episode["id"],
                    "aired": episode["aired"],
                }
                clean_ep_list.append(clean_ep)

        return clean_ep_list
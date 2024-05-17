"""
    This module contains TVDBUtils class.
"""

from typing import Callable

from plexutils.api.tvdb_api import TvdbApi
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.menu import Menu
from plexutils.shared.utils import print_menu


class TVDBUtils:
    """represents the menu and tools with tvdb"""

    def __init__(self, config: dict, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: dict = config

        if "tvdb-key" in self.config:
            self.tvdb_key = self.config["tvdb-key"]
        if "tvdb-pin" in self.config:
            self.tvdb_pin = self.config["tvdb-pin"]

        self.menu_list: Menu = Menu(
            [
                {
                    "id": "1",
                    "name": self.gettext(
                        "search in tvdb for new seasons of existing tvshows"
                    ),
                    "action": self.search_new_seasons,
                },
                {
                    "id": "2",
                    "name": self.gettext(
                        "search in tvdb for missing episodes of existing seasons of"
                        + " existing tvshows"
                    ),
                    "action": self.search_missing_episodes,
                },
            ]
        )

    def get_utils_name(self) -> str:
        """returns the utils name"""
        return self.gettext(
            "TVDBUtils       - Tools to compare the plex library with tvdb or search new content"
        )

    def print_menu(self) -> None:
        """prints the menu"""
        print_menu(self.gettext("TVDBUtils Menu:"), self.gettext, self.menu_list)

    def search_new_seasons(self) -> None:
        """
        searches for new seasons
            of existing tvshows
        """
        if "tvshows-dir" not in self.config:
            return

        tvdb_api: TvdbApi = TvdbApi(self.tvdb_key, self.tvdb_pin)
        crawler: PlexTVShowCrawler = PlexTVShowCrawler(self.config["tvshows-dir"])
        crawler.crawl()

        tvshows: list[TVShow] = crawler.get_tvshowlist().tvshows
        missing_season_strings: list[str] = []
        for tvshow in tvshows:
            plex_tvshow_seasonids: set[int] = set(tvshow.seasonids)
            tvdb_tvshow_seasonids: set[int] = tvdb_api.get_seasonids(tvshow.tvdbid)
            missing_seasons: list[int] = list(
                tvdb_tvshow_seasonids - plex_tvshow_seasonids
            )
            for missing_season in missing_seasons:
                missing_season_strings.append(f"{tvshow.dirname} -> {missing_season}")

        for season in missing_season_strings:
            print(season)

        input(self.gettext("Press Enter to continue..."))

    def search_missing_episodes(self) -> None:
        """
        searches for missing episodes
            of existing seasons
            of existing tvshows
        """
        if "tvshows-dir" not in self.config:
            return

        tvdb_api: TvdbApi = TvdbApi(self.tvdb_key, self.tvdb_pin)
        crawler: PlexTVShowCrawler = PlexTVShowCrawler(self.config["tvshows-dir"])
        crawler.crawl()

        tvshows: list[TVShow] = crawler.get_tvshowlist().tvshows
        missing_episode_strings: list[str] = []
        for tvshow in tvshows:
            seasons: list[TVShowSeason] = tvshow.seasons
            for season in seasons:
                plex_episodeids: set[int] = set(season.episodeids)
                tvdb_episodeids: set[int] = tvdb_api.get_episodeids(
                    tvshow.tvdbid, season.season_id
                )

                missing_episodes: list[int] = list(tvdb_episodeids - plex_episodeids)
                for missing_episode in missing_episodes:
                    missing_episode_strings.append(
                        f"{tvshow.dirname} -> s{season.season_id}e{missing_episode}"
                    )

        for episode in missing_episode_strings:
            print(episode)

        input(self.gettext("Press Enter to continue..."))

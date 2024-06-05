"""
    This module contains TVDBUtils class.
"""

from typing import Callable

from plexutils.api.tvdb_api import TvdbApi
from plexutils.config.config import Config
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.console_menu import ConsoleMenu
from plexutils.shared.menu_tools import library_menu_wrapper, print_menu


class TVDBUtils:
    """represents the menu and tools with tvdb"""

    def __init__(self, config: Config, gettext: Callable[[str], str]):
        self.gettext: Callable[[str], str] = gettext
        self.config: Config = config
        self.tvdb_key: str = ""
        self.tvdb_pin: str = ""

        if self.config is not None and self.config.tvdb is not None:
            if self.config.tvdb.api_key is not None:
                self.tvdb_key = self.config.tvdb.api_key
            if self.config.tvdb.api_pin is not None:
                self.tvdb_pin = self.config.tvdb.api_pin

        self.menu_list: ConsoleMenu = ConsoleMenu(
            [
                {
                    "id": "1",
                    "name": self.gettext(
                        "search in tvdb for new seasons of existing tvshows"
                    ),
                    "action": lambda: library_menu_wrapper(
                        self.gettext, self.config, "tvshow", self.search_new_seasons
                    ),
                },
                {
                    "id": "2",
                    "name": self.gettext(
                        "search in tvdb for missing episodes of existing seasons of"
                        + " existing tvshows"
                    ),
                    "action": lambda: library_menu_wrapper(
                        self.gettext,
                        self.config,
                        "tvshow",
                        self.search_missing_episodes,
                    ),
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

    def search_new_seasons(self, library_path: str) -> None:
        """
        searches for new seasons
            of existing tvshows
        """

        tvdb_api: TvdbApi = TvdbApi(self.tvdb_key, self.tvdb_pin)
        crawler: PlexTVShowCrawler = PlexTVShowCrawler(library_path)
        crawler.crawl()

        tvshows: list[TVShow] = crawler.get_tvshowlist().tvshows
        missing_season_strings: list[str] = []
        for tvshow in tvshows:
            if tvshow.tvdbid is None:
                raise ValueError()

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

    def search_missing_episodes(self, library_path: str) -> None:
        """
        searches for missing episodes
            of existing seasons
            of existing tvshows
        """

        tvdb_api: TvdbApi = TvdbApi(self.tvdb_key, self.tvdb_pin)
        crawler: PlexTVShowCrawler = PlexTVShowCrawler(library_path)
        crawler.crawl()

        tvshows: list[TVShow] = crawler.get_tvshowlist().tvshows
        missing_episode_strings: list[str] = []
        for tvshow in tvshows:
            if tvshow.tvdbid is None:
                raise ValueError()

            seasons: list[TVShowSeason] = tvshow.seasons
            for season in seasons:
                if season.season_id is None:
                    raise ValueError()

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

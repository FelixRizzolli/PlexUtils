"""
    This module contains TVDBUtils class.
"""

from typing import Optional

from plexutils.api.tvdb_api import TvdbApi
from plexutils.console.menu import ConsoleMenu
from plexutils.crawler.plex_tvshow_crawler import PlexTVShowCrawler
from plexutils.media.tvshow import TVShow
from plexutils.media.tvshow_season import TVShowSeason
from plexutils.shared.menu_tools import library_menu_wrapper


class TVDBUtils(ConsoleMenu):
    """represents the menu and tools with tvdb"""

    def __init__(self):
        super().__init__()
        self.title = self.gettext("TVDBUtils Menu:")
        self.setup_menu()

        self.tvdb_key: str = ""
        self.tvdb_pin: str = ""

        if self.config is not None and self.config.tvdb is not None:
            if self.config.tvdb.api_key is not None:
                self.tvdb_key = self.config.tvdb.api_key
            if self.config.tvdb.api_pin is not None:
                self.tvdb_pin = self.config.tvdb.api_pin

    def setup_menu(self) -> None:
        """
        sets up the menu items

        :return: None
        """
        self.add_item(
            {
                "id": "1",
                "name": self.gettext(
                    "search in tvdb for new seasons of existing tvshows"
                ),
                "action": lambda: library_menu_wrapper(
                    self.gettext, self.config, "tvshow", self.search_new_seasons
                ),
            }
        )
        self.add_item(
            {
                "id": "2",
                "name": self.gettext(
                    "search in tvdb for missing episodes of existing seasons of existing tvshows"
                ),
                "action": lambda: library_menu_wrapper(
                    self.gettext,
                    self.config,
                    "tvshow",
                    self.search_missing_episodes,
                ),
            },
        )

    def get_utils_name(self) -> str:
        """
        returns the utils name

        :return: The utils name.
        :rtype: str
        """
        return self.gettext(
            "TVDBUtils       - Tools to compare the plex library with tvdb or search new content"
        )

    def search_new_seasons(self, library_path: str) -> None:
        """
        searches for new seasons
            of existing tvshows

        :param library_path: The path of the library.
        :type library_path: str

        :return: None
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

        :param library_path: The path of the library.
        :type library_path: str

        :return: None
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

    def check_config(self) -> Optional[str]:
        """
        Checks the configuration and returns a warning message if needed.

        :return: The warning message.
        :rtype: Optional[str]
        """

        if self.config is None:
            return self.gettext("No config found")
        if self.config.tvdb is None:
            return self.gettext("No TVDB credentials found")
        if self.config.tvdb.api_key is None:
            return self.gettext("No TVDB api key found")
        if self.config.tvdb.api_pin is None:
            return self.gettext("No TVDB api pin found")
        if len(self.config.get_tvshow_libraries()) == 0:
            return self.gettext("No tvshow libraries found")

        return None

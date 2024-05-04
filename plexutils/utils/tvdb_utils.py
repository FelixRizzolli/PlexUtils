from shared.plex_tvshow_crawler import PlexTvshowCrawler
from shared.menu import Menu
from shared.utils import print_menu
from shared.tvdb_tool import TVDBTool


class TVDBUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        if 'tvdb-key' in self.config:
            self.tvdb_key = self.config['tvdb-key']
        if 'tvdb-pin' in self.config:
            self.tvdb_pin = self.config['tvdb-pin']

        self.menu_list = Menu([
            {
                'id': '1',
                'name': "search in tvdb for new seasons of existing tvshows",
                'action': self.search_new_seasons,
            },
            {
                'id': '2',
                'name': "search in tvdb for missing episodes of existing seasons of existing tvshows",
                'action': self.search_missing_episodes,
            },
        ])

    def get_utils_name(self):
        return self.gettext("TVDBUtils - Tools to compare the plex library with tvdb or search new content")

    def print_menu(self):
        print_menu(self.gettext("TVDBUtils Menu:"), self.gettext, self.menu_list)

    def search_new_seasons(self):
        if 'tvshows-dir' not in self.config:
            return False

        tvdb_tool = TVDBTool(self.tvdb_key, self.tvdb_pin)
        crawler = PlexTvshowCrawler(self.config['tvshows-dir'])
        crawler.crawl()

        tvshows = crawler.get_tvshowlist().get_tvshows()
        missing_season_strings = []
        for tvshow in tvshows:
            plex_tvshow_seasonids = set(tvshow.get_seasonids())
            tvdb_tvshow_seasonids = tvdb_tool.get_seasonids(tvshow.get_tvdbid())
            missing_seasons = list(tvdb_tvshow_seasonids - plex_tvshow_seasonids)
            for missing_season in missing_seasons:
                missing_season_strings.append(f'{tvshow.get_dirname()} -> {missing_season}')

        for season in missing_season_strings:
            print(season)

        input(self.gettext("Press Enter to continue..."))


    def search_missing_episodes(self):
        if 'tvshows-dir' not in self.config:
            return False

        tvdb_tool = TVDBTool(self.tvdb_key, self.tvdb_pin)
        crawler = PlexTvshowCrawler(self.config['tvshows-dir'])
        crawler.crawl()

        tvshows = crawler.get_tvshowlist().get_tvshows()
        missing_episode_strings = []
        for tvshow in tvshows:
            seasons = tvshow.get_seasons()
            for season in seasons:
                plex_episodeids = set(season.get_episodeids())
                tvdb_episodeids = tvdb_tool.get_episodeids(tvshow.get_tvdbid(), season.get_id())

                missing_episodes = list(tvdb_episodeids - plex_episodeids)
                for missing_episode in missing_episodes:
                    missing_episode_strings.append(
                        f"{tvshow.get_dirname()} -> s{season.get_id()}e{missing_episode}"
                    )

        for episode in missing_episode_strings:
            print(episode)

        input(self.gettext("Press Enter to continue..."))

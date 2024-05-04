from plexutils.shared.menu import Menu
from plexutils.shared.utils import print_menu
from plexutils.shared.plex_tvshow_crawler import PlexTvshowCrawler


class TvshowFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.menu_list = Menu([
            {
                'id': '1',
                'name': self.gettext("validate tvshow directory syntax"),
                'action': self.validate_tvshow_syntax,
            },
            {
                'id': '2',
                'name': self.gettext("validate season directory syntax"),
                'action': self.validate_season_syntax,
            },
            {
                'id': '3',
                'name': self.gettext("validate episode filename syntax"),
                'action': self.validate_episode_syntax,
            },
        ])

    def get_utils_name(self):
        return self.gettext("TvshowFileUtils - Tools for tvshow directories and episode files")

    def print_menu(self):
        print_menu(self.gettext("TvshowFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_tvshow_syntax(self):
        if 'tvshows-dir' not in self.config:
            return False

        crawler = PlexTvshowCrawler(self.config['tvshows-dir'])
        crawler.crawl()

        for tvshow in crawler.get_invalid_tvshows():
            print(self.gettext("Invalid tvshow directory: ") + tvshow)

        input()

    def validate_season_syntax(self):
        if 'tvshows-dir' not in self.config:
            return False

        crawler = PlexTvshowCrawler(self.config['tvshows-dir'])
        crawler.crawl()

        for season in crawler.get_invalid_seasons():
            print(self.gettext("Invalid season directory: ") + season)

        input()

    def validate_episode_syntax(self):
        if 'tvshows-dir' not in self.config:
            return False

        crawler = PlexTvshowCrawler(self.config['tvshows-dir'])
        crawler.crawl()

        for episode in crawler.get_invalid_episodes():
            print(self.gettext("Invalid episode filename: ") + episode)

        input()

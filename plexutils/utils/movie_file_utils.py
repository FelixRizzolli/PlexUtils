from shared.menu import Menu
from shared.utils import print_menu
from shared.plex_movie_crawler import PlexMovieCrawler


class MovieFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.menu_list = Menu([
            {
                'id': '1',
                'name': self.gettext("validate movie filename syntax"),
                'action': self.validate_movie_syntax,
            },
        ])

    def get_utils_name(self):
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self):
        print_menu(self.gettext("MovieFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_movie_syntax(self):
        if 'movies-dir' not in self.config:
            return False

        crawler = PlexMovieCrawler(self.config['movies-dir'])
        crawler.crawl()

        for movie in crawler.get_invalid_movies():
            print(self.gettext("Invalid movie file: ") + movie)

        input()

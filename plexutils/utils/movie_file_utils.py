from plexutils.shared.menu import Menu
from plexutils.shared.utils import print_menu
from plexutils.shared.plex_movie_crawler import PlexMovieCrawler


class MovieFileUtils:
    """represents the menu and tools for movie files"""

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
        """returns the utils name"""
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self):
        """prints the menu"""
        print_menu(self.gettext("MovieFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_movie_syntax(self):
        """
            validates the filenames
                of the movies
                from the initialized directory
        """
        if 'movies-dir' not in self.config:
            return False

        crawler = PlexMovieCrawler(self.config['movies-dir'])
        crawler.crawl()

        for movie in crawler.get_invalid_movies():
            print(self.gettext("Invalid movie file: ") + movie)

        input()

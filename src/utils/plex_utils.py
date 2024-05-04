from .movie_file_utils import MovieFileUtils
from .tvshow_file_utils import TvshowFileUtils
from .tvdb_utils import TVDBUtils
from shared.menu import Menu
from shared.utils import print_menu

class PlexUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.movie_file_utils = MovieFileUtils(config, gettext)
        self.tvshow_file_utils = TvshowFileUtils(config, gettext)
        self.tvdb_utils = TVDBUtils(config, gettext)

        self.menu_list = Menu([
            {
                'id': '1',
                'name': self.movie_file_utils.get_utils_name(),
                'action': self.movie_file_utils.print_menu,
            },
            {
                'id': '2',
                'name': self.tvshow_file_utils.get_utils_name(),
                'action': self.tvshow_file_utils.print_menu,
            },
            {
                'id': '3',
                'name': self.tvdb_utils.get_utils_name(),
                'action': self.tvdb_utils.print_menu,
            },
        ])

    def print_menu(self):
        print_menu(self.gettext("PlexUtils Menu:"), self.gettext, self.menu_list)

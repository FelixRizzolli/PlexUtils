from shared.menu import Menu
from shared.utils import print_menu


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
                "id": "1",
                "name": "search in tvdb for new seasons of existing tvshows",
                "action": self.search_new_seasons,
            },
            {
                "id": "2",
                "name": "search in tvdb for missing episodes of existing seasons of existing tvshows",
                "action": self.search_missing_episodes,
            },
        ])

    def get_utils_name(self):
        return self.gettext("TVDBUtils - Tools to compare the plex library with tvdb or search new content")

    def print_menu(self):
        print_menu(self.gettext("TVDBUtils Menu:"), self.gettext, self.menu_list)

    def search_new_seasons(self):
        pass

    def search_missing_episodes(self):
        pass

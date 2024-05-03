from shared.menu import Menu
from shared.utils import print_menu


class MovieFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.menu_list = Menu([
            {
                "id": "1",
                "name": self.gettext("validate movie filename syntax"),
                "action": self.get_utils_name,
            },
        ])

    def get_utils_name(self):
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self):
        print_menu(self.gettext("MovieFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_movie_syntax(self):
        pass
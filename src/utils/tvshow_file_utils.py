from shared.menu import Menu
from shared.utils import print_menu

class TvshowFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.menu_list = Menu([
            {
                "id": "1",
                "name": self.gettext("validate tvshow directory syntax"),
                "action": self.get_utils_name,
            },
            {
                "id": "2",
                "name": self.gettext("validate season directory syntax"),
                "action": self.get_utils_name,
            },
            {
                "id": "3",
                "name": self.gettext("validate episode filename syntax"),
                "action": self.get_utils_name,
            },
        ])

    def get_utils_name(self):
        return self.gettext("TvshowFileUtils - Tools for tvshow directories and episode files")

    def print_menu(self):
        print_menu(self.gettext("TvshowFileUtils Menu:"), self.gettext, self.menu_list)

    def validate_tvshow_syntax(self):
        pass

    def validate_season_syntax(self):
        pass

    def validate_episode_syntax(self):
        pass

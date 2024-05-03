from shared.menu import clear_console


class MovieFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

    def get_utils_name(self):
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self):
        clear_console()
        print("Movie File Utilities")


class MovieFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

    def get_utils_name(self):
        return self.gettext("MovieFileUtils  - Tools for movie files")

    def print_menu(self):
        print("Movie File Utilities")
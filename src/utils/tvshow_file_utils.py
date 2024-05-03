from shared.menu import clear_console


class TvshowFileUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

    def get_utils_name(self):
        return self.gettext("TvshowFileUtils - Tools for tvshow directories and episode files")

    def print_menu(self):
        clear_console()
        print("Tvshow File Utilities")

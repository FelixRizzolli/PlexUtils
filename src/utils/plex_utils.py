from movie_file_utils import MovieFileUtils
from tvshow_file_utils import TvshowFileUtils
from shared.menu import Menu

class PlexUtils:
    def __init__(self, config, gettext):
        self.gettext = gettext
        self.config = config

        self.movie_file_utils = MovieFileUtils(config, gettext)
        self.tvshow_file_utils = TvshowFileUtils(config, gettext)

        self.menu_list = Menu([
            {
                "id": "1",
                "name": self.movie_file_utils.get_utils_name(),
                "action": self.movie_file_utils.print_menu,
            },
            {
                "id": "2",
                "name": self.tvshow_file_utils.get_utils_name(),
                "action": self.tvshow_file_utils.print_menu,
            },
        ])

    def print_menu(self):
        while True:
            print("\n" + self.gettext("PlexUtils Menu:"))
            for option in self.menu_list.get_list():
                print(f"{option["id"]}. {option["name"]}")

            choice = input("\n" + self.gettext("Enter your choice: "))

            if self.menu_list.id_exists(choice):
                self.menu_list.get_option_by_id(choice)["action"]()
            else:
                print("\n" + self.gettext("Invalid choice. Please enter a valid option."))

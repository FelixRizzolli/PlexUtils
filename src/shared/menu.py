import os


def clear_console():
    print("clear_console()")
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)


class Menu(object):
    def __init__(self, menu):
        self.menu = menu

    def id_exists(self, option_id):
        for item in self.menu:
            if item['id'] == option_id:
                return True
        return False

    def get_option_by_id(self, option_id):
        for option in self.menu:
            if option['id'] == option_id:
                return option
        return None

    def get_list(self):
        return self.menu

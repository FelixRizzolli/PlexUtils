import os


def clear_console():
    print("clear_console()")
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)


class Menu(object):
    def __init__(self, menu_list):
        self.menu_list = menu_list

    def id_exists(self, option_id):
        for item in self.menu_list:
            if item['id'] == option_id:
                return True
        return False

    def get_option_by_id(self, option_id):
        for option in self.menu_list:
            if option['id'] == option_id:
                return option
        return None

    def get_list(self):
        return self.menu_list

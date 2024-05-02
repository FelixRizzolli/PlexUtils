from shared.menu import Menu
import gettext
import os
import yaml

# Get the current script directory
current_script_dir = os.path.dirname(os.path.realpath(__file__))

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def setup_i18n():
    # Construct the path to the locale directory
    locale_dir = os.path.join(os.path.dirname(current_script_dir), 'locale')

    language = "en_US"
    if 'language' in config:
        language = config['language']

    trans = gettext.translation('plexutils', locale_dir, [language], fallback=True)
    trans.install()
    return trans.gettext


def option_1():
    print("\n" + _("You selected Option 1."))


def menu():
    menu_list = Menu([
        {"id": "1", "name": _("Option 1"), "action": option_1}
    ])

    while True:
        print("\n" + _("Console Menu:"))
        for option in menu_list.get_list():
            print(f"{option["id"]}. {option["name"]}")

        choice = input("\n" + _("Enter your choice: "))

        if menu_list.id_exists(choice):
            menu_list.get_option_by_id(choice)["action"]()
        else:
            print("\n" + _("Invalid choice. Please enter a valid option."))


if __name__ == '__main__':
    config_dir = os.path.join(os.path.dirname(current_script_dir) + '/config.yaml')
    config = load_config(config_dir)
    _ = setup_i18n()
    menu()

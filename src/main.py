import gettext
import os
import yaml

from plex_utils import PlexUtils

def load_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def setup_i18n(pj_path, config):
    locale_dir = os.path.join(pj_path, 'locale')

    language = "en_US"
    if (config is not None) and ('language' in config):
        language = config['language']

    trans = gettext.translation('plexutils', locale_dir, [language], fallback=True)
    trans.install()
    return trans.gettext


if __name__ == '__main__':
    pj_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config_dir = os.path.join(pj_path + '/config.yaml')
    config = load_config(config_dir)

    gettext = setup_i18n(pj_path, config)

    plex_utils = PlexUtils(config, gettext)
    plex_utils.print_menu()

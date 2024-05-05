import os

from plexutils.utils.plex_utils import PlexUtils
from plexutils.shared.utils import load_config, setup_i18n


if __name__ == '__main__':
    pj_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config_dir = os.path.join(pj_path + '/config.yaml')
    config = load_config(config_dir)

    gettext = setup_i18n(pj_path, config)

    plex_utils = PlexUtils(config, gettext)
    plex_utils.print_menu()

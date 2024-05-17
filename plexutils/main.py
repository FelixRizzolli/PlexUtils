"""
    This module contains the main function.
"""

import os
from typing import Callable

from plexutils.shared.utils import load_config, setup_i18n
from plexutils.utils.plex_utils import PlexUtils

if __name__ == "__main__":
    pj_path: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config_dir: str = os.path.join(pj_path + "/config.yaml")
    config: dict = load_config(config_dir)

    gettext: Callable[[str], str] = setup_i18n(pj_path, config)

    plex_utils: PlexUtils = PlexUtils(config, gettext)
    plex_utils.print_menu()

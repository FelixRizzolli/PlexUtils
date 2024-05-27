"""
    This module contains the main function.
"""

import os
from typing import Callable

from plexutils.config.config import Config
from plexutils.shared.config_tools import load_config, setup_i18n
from plexutils.utils.plex_utils import PlexUtils


def main() -> None:
    """
    Main function of the project.
    """
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..")
    config_file: str = os.path.join(pj_path, "config.yaml")

    config: Config = load_config(config_file)

    gettext: Callable[[str], str] = setup_i18n(pj_path, config)

    plex_utils: PlexUtils = PlexUtils(config, gettext)
    plex_utils.print_menu()


if __name__ == "__main__":
    main()

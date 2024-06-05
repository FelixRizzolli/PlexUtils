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

    # Get the path of the script and the project
    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..")

    # Load the configuration
    config: Config = load_config()

    # Setup internationalization
    gettext: Callable[[str], str] = setup_i18n(pj_path, config)

    # Create a PlexUtils object and print the main menu
    plex_utils: PlexUtils = PlexUtils(config, gettext)
    plex_utils.print_menu()


if __name__ == "__main__":
    main()

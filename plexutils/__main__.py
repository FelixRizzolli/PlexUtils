"""
    This module contains the main function.
"""

from plexutils.utils.plex_utils import PlexUtils


def main() -> None:
    """
    Main function of the project.
    """
    plex_utils: PlexUtils = PlexUtils()
    plex_utils.print_menu()


if __name__ == "__main__":
    main()

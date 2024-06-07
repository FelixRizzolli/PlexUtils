"""
This module contains the Config class which represents the configuration for the application.
"""

from dataclasses import dataclass

from plexutils.config.plex_library_infos import PlexLibraryInfos, PlexLibraryType
from plexutils.config.tvdb_credentials import TVDBCredentials


@dataclass
class Config:
    """
    Represents the configuration for the application.
    """

    language: str
    libraries: list[PlexLibraryInfos]
    tvdb: TVDBCredentials

    def get_movie_libraries(self):
        """
        Get all movie libraries from the configuration.

        Returns:
            list[PlexLibraryInfos]: A list of PlexLibraryInfos objects representing
                                    movie libraries.
        """
        return [lib for lib in self.libraries if lib.type == PlexLibraryType.MOVIE]

    def get_tvshow_libraries(self):
        """
        Get all TV show libraries from the configuration.

        Returns:
            list[PlexLibraryInfos]: A list of PlexLibraryInfos objects representing
                                    TV show libraries.
        """
        return [lib for lib in self.libraries if lib.type == PlexLibraryType.TVSHOW]

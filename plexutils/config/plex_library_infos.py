"""
This module contains the PlexLibraryInfos class which is used to store and manage
information about a Plex library.
"""

from dataclasses import dataclass
from enum import Enum


class PlexLibraryType(Enum):
    """
    An enumeration representing the type of the Plex library.
    """

    MOVIE = "movie"
    TVSHOW = "tvshow"


@dataclass
class PlexLibraryInfos:
    """
    Represents information about a Plex library.
    """

    type: PlexLibraryType
    name: str
    path: str
    dub_lang: str = ""
    sub_lang: str = ""

    @property
    def full_name(self) -> str:
        """
        Get the full name of the Plex library.

        The full name is constructed from the dubbing language, subtitle language,
        and the name of the library.

        :return: The full name of the Plex library.
        :rtype: str
        """
        _full_name: str = ""

        if len(self.dub_lang) == 5:
            _full_name += f"({self.dub_lang[3:5].upper()}"
        elif len(self.dub_lang) == 2:
            _full_name += f"({self.dub_lang.upper()}"
        else:
            _full_name += "(EN"

        if len(self.sub_lang) == 5:
            _full_name += f"-{self.sub_lang[3:5].upper()})"
        elif len(self.sub_lang) == 2:
            _full_name += f"-{self.sub_lang.upper()})"
        else:
            _full_name += ")"

        _full_name += f" {self.name}"

        return _full_name

    def to_dict(self) -> dict:
        """
        Convert the PlexLibraryInfos object to a dictionary.

        :return: A dictionary representation of the PlexLibraryInfos object.
        :rtype: dict
        """
        return {
            "type": self.type.value,
            "name": self.name,
            "path": self.path,
            "lang": {"dub": self.dub_lang, "sub": self.sub_lang},
        }

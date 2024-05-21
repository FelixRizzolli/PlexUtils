"""
This module contains the PlexLibraryInfos class which is used to store and manage
information about a Plex library.
"""


class PlexLibraryInfos:
    """
    Represents information about a Plex library.
    """

    def __init__(
        self, type: str, name: str, path: str, dub_lang: str = "", sub_lang: str = ""
    ):
        """
        Initializes a new instance of the PlexLibraryInfos class.
        """
        self._type: str = type
        self._name: str = name
        self._path: str = path
        self._dub_lang: str = dub_lang
        self._sub_lang: str = sub_lang

    @property
    def type(self) -> str:
        """
        Gets the type of the Plex library.

        Returns:
            str: The type of the Plex library.
        """
        return self._type

    @property
    def name(self) -> str:
        """
        Gets the name of the Plex library.

        Returns:
            str: The name of the Plex library.
        """
        return self._name

    @property
    def path(self) -> str:
        """
        Gets the path of the Plex library.

        Returns:
            str: The path of the Plex library.
        """
        return self._path

    @property
    def dub_lang(self) -> str:
        """
        Gets the dubbing language of the Plex library.

        Returns:
            str: The dubbing language of the Plex library.
        """
        return self._dub_lang

    @property
    def sub_lang(self) -> str:
        """
        Gets the subtitle language of the Plex library.

        Returns:
            str: The subtitle language of the Plex library.
        """
        return self._sub_lang

    @property
    def full_name(self) -> str:
        """
        Gets the full name of the Plex library, including the dubbing and subtitle languages.

        Returns:
            str: The full name of the Plex library.
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

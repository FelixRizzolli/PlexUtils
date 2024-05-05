"""
    This module contains Movie class.
"""
from typing import Optional

from plexutils.shared.utils import extract_tvdbid


class Movie:
    """represents a single movie"""
    def __init__(self, filename: str):
        self.filename: str = filename
        self.tvdbid: Optional[int] = extract_tvdbid(filename)

    def get_tvdbid(self) -> Optional[int]:
        """returns the tvdbid of the movie"""
        return self.tvdbid

    def get_filename(self) -> str:
        """return the filename of the movie"""
        return self.filename

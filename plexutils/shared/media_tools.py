"""
This module contains utility functions for extracting specific information from directory
and file names. These functions are primarily used for handling media files in a Plex server
setup.
"""

import re
from typing import Optional


def extract_tvdbid(dirname: str) -> Optional[int]:
    """
    Extracts the TVDB ID from a directory name.

    Parameters:
        dirname (str): The directory name.

    Returns:
        Optional[int]: The TVDB ID if found, None otherwise.
    """
    tvdbid_pattern: str = r"{tvdb-(\d+)}"
    tvdbid_match: Optional[re.Match] = re.search(tvdbid_pattern, dirname)

    if tvdbid_match:
        return int(tvdbid_match.group(1))
    return None


def extract_episodeid(filename: str) -> Optional[int]:
    """
    Extracts the episode ID from a file name.

    Parameters:
        filename (str): The file name.

    Returns:
        Optional[int]: The episode ID if found, None otherwise.
    """
    episodeid_pattern: str = r"- s(\d+)e(\d+)"
    episodeid_match: Optional[re.Match] = re.search(episodeid_pattern, filename)

    if episodeid_match:
        return int(episodeid_match.group(2))
    return None


def extract_seasonid_from_episode(filename: str) -> Optional[int]:
    """
    Extracts the season ID from a file name.

    Parameters:
        filename (str): The file name.

    Returns:
        Optional[int]: The season ID if found, None otherwise.
    """
    seasonid_pattern: str = r"- s(\d+)e(\d+)"
    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, filename)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def extract_seasonid(dirname: str) -> Optional[int]:
    """
    Extracts the season ID from a directory name.

    Parameters:
        dirname (str): The directory name.

    Returns:
        Optional[int]: The season ID if found, None otherwise.
    """
    seasonid_pattern: str = r"season (\d+)"
    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, dirname)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None

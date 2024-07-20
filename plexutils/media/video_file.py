"""
This module contains the VideoFile class.
"""

import os.path
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class VideoFile:
    """
    Represents a single video file.
    """

    _filepath: str
    _filesize: int
    _duration: int
    _resolution_width: int
    _resolution_height: int
    _video_codec: str
    _audio_codec: str

    @property
    def filename(self) -> str:
        """
        Returns the filename of the video file.

        :return: The filename of the video file.
        :rtype: str
        """
        return os.path.basename(self._filepath)

    @property
    def filepath(self) -> str:
        """
        Returns the filepath of the video file.

        :return: The filepath of the video file.
        :rtype: str
        """
        return self._filepath

    @property
    def filesize(self) -> int:
        """
        Returns the filesize of the video file.

        :return: The filesize of the video file.
        :rtype: int
        """
        return self._filesize

    @property
    def duration(self) -> int:
        """
        Returns the duration of the video file.

        :return: The duration of the video file.
        :rtype: int
        """
        return self._duration

    @property
    def resolution_width(self) -> int:
        """
        Returns the resolution width of the video file.

        :return: The resolution width of the video file.
        :rtype: int
        """
        return self._resolution_width

    @property
    def resolution_height(self) -> int:
        """
        Returns the resolution height of the video file.

        :return: The resolution height of the video file.
        :rtype: int
        """
        return self._resolution_height

    @property
    def video_codec(self) -> str:
        """
        Returns the video codec of the video file.

        :return: The video codec of the video file.
        :rtype: str
        """
        return self._video_codec

    @property
    def audio_codec(self) -> str:
        """
        Returns the audio codec of the video file.

        :return: The audio codec of the video file.
        :rtype: str
        """
        return self._audio_codec

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks if the video file has a valid filename.

        :return: True if the video file has a valid filename, False otherwise.
        :rtype: bool
        """
        pass

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
    _format_name: str
    _filesize: int
    _duration: float
    _resolution_width: int
    _resolution_height: int
    _video_codec: str
    _audio_codec: str
    _bitrate: int
    _frame_rate: int
    _number_of_streams: int
    _pixel_format: str

    @property
    def __dict__(self) -> dict:
        return {
            "filename": self.filename,
            "format_name": self.format_name,
            "filepath": self.filepath,
            "filesize": self.filesize,
            "duration": self.duration,
            "resolution_width": self.resolution_width,
            "resolution_height": self.resolution_height,
            "video_codec": self.video_codec,
            "audio_codec": self.audio_codec,
            "bitrate": self.bitrate,
            "frame_rate": self.frame_rate,
            "number_of_streams": self.number_of_streams,
            "pixel_format": self.pixel_format,
        }

    @property
    def filename(self) -> str:
        """
        Returns the filename of the video file.

        :return: The filename of the video file.
        :rtype: str
        """
        return os.path.basename(self._filepath)

    @property
    def format_name(self) -> str:
        """
        Returns the format name of the video file.

        :return: The format name of the video file.
        :rtype: str
        """
        return self._format_name

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

    @property
    def bitrate(self) -> int:
        """
        Returns the bitrate of the video file.

        :return: The bitrate of the video file.
        :rtype: int
        """
        return self._bitrate

    @property
    def frame_rate(self) -> int:
        """
        Returns the frame rate of the video file.

        :return: The frame rate of the video file.
        :rtype: int
        """
        return self._frame_rate

    @property
    def number_of_streams(self) -> int:
        """
        Returns the number of streams in the video file.

        :return: The number of streams in the video file.
        :rtype: int
        """
        return self._number_of_streams

    @property
    def pixel_format(self) -> str:
        """
        Returns the pixel format of the video file.

        :return: The pixel format of the video file.
        :rtype: str
        """
        return self._pixel_format

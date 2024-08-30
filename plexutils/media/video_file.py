"""
This module contains the VideoFile class.
"""

import os.path
from abc import abstractmethod
from typing import Any

import ffmpeg


class VideoFile:
    """
    Represents a single video file.
    """

    _probe: Any
    _video_stream: Any

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

    def __init__(self, file_path: str):
        self._filepath = file_path

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
    def duration(self) -> float:
        """
        Returns the duration of the video file.

        :return: The duration of the video file.
        :rtype: float
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

    def collect_data(self):
        """
        Collects the video file data.

        :return: None
        """
        self._probe = ffmpeg.probe(self._filepath)
        self._video_stream = next(stream for stream in self._probe["streams"])

        self._read_format_name()
        self._read_filesize()
        self._read_video_codec()
        self._read_audio_codec()
        self._read_duration()
        self._read_resolution()
        self._read_bitrate()
        self._read_frame_rate()
        self._read_number_of_streams()
        self._read_pixel_format()

    def _read_filesize(self) -> None:
        """
        Get the filesize of the video file.

        :return: None
        """
        try:
            self._filesize = os.path.getsize(self._filepath)
        except Exception:
            self._filesize = 0

    def _read_video_codec(self) -> None:
        """
        Read the video codec from the video stream.

        :return: None
        """
        try:
            self._video_codec = self._video_stream["codec_name"]
        except Exception:
            self._video_codec = "unknown"

    def _read_audio_codec(self) -> None:
        """
        Get the audio codec from the video stream.

        :return: None
        """
        try:
            self._audio_codec = self._video_stream["codec_name"]
        except Exception:
            self._audio_codec = "unknown"

    def _read_duration(self) -> None:
        """
        Get the duration of the video file.

        :return: None
        """
        try:
            self._duration = float(self._probe["format"]["duration"])
        except Exception:
            self._duration = 0.0

    def _read_resolution(self) -> None:
        """
        Get the resolution of the video file.

        :return: None
        """
        try:
            self._resolution_width = int(self._video_stream["width"])
            self._resolution_height = int(self._video_stream["height"])
        except Exception:
            self._resolution_width = 0
            self._resolution_height = 0

    def _read_bitrate(self) -> None:
        """
        Get the bitrate of the video file.

        :return: None
        """
        try:
            self._bitrate = int(self._video_stream["bit_rate"]) // 1000
        except Exception:
            self._bitrate = 0

    def _read_frame_rate(self) -> None:
        """
        Get the frame rate of the video file.

        :return: None
        """
        try:
            self._frame_rate = int(self._video_stream["r_frame_rate"].split("/")[0])
        except Exception:
            self._frame_rate = 0

    def _read_format_name(self) -> None:
        """
        Get the format name of the video file.

        :return: None
        """
        try:
            self._format_name = self._probe["format"]["format_name"]
        except Exception:
            self._format_name = "unknown"

    def _read_number_of_streams(self) -> None:
        """
        Get the number of streams in the video file.

        :return: None
        """
        try:
            self._number_of_streams = len(self._probe["streams"])
        except Exception:
            self._number_of_streams = 0

    def _read_pixel_format(self) -> None:
        """
        Get the pixel format of the video file.

        :return: None
        """
        try:
            self._pixel_format = self._video_stream["pix_fmt"]
        except Exception:
            self._pixel_format = "unknown"

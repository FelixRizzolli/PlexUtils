"""
This module contains utility functions for extracting specific information from directory
and file names. These functions are primarily used for handling media files in a Plex server
setup.
"""

import os
import re
from typing import Optional

import ffmpeg

from video_file import VideoFile


def extract_tvdbid(dirname: str) -> Optional[int]:
    """
    Extracts the TVDB ID from a directory name.

    :param dirname: The directory name.
    :type dirname: str

    :return: The TVDB ID if found, None otherwise.
    :rtype: Optional[int]
    """
    tvdbid_pattern: str = r"{tvdb-(\d+)}"
    tvdbid_match: Optional[re.Match] = re.search(tvdbid_pattern, dirname)

    if tvdbid_match:
        return int(tvdbid_match.group(1))
    return None


def extract_episodeid(filename: str) -> Optional[int]:
    """
    Extracts the episode ID from a file name.

    :param filename: The file name.
    :type filename: str

    :return: The episode ID if found, None otherwise.
    :rtype: Optional[int]
    """
    episodeid_pattern: str = r"- s(\d+)e(\d+)"
    episodeid_match: Optional[re.Match] = re.search(episodeid_pattern, filename)

    if episodeid_match:
        return int(episodeid_match.group(2))
    return None


def extract_seasonid_from_episode(filename: str) -> Optional[int]:
    """
    Extracts the season ID from a file name.

    :param filename: The file name.
    :type filename: str

    :return: The season ID if found, None otherwise.
    :rtype: Optional[int]
    """
    seasonid_pattern: str = r"- s(\d+)e(\d+)"
    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, filename)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def extract_seasonid(dirname: str) -> Optional[int]:
    """
    Extracts the season ID from a directory name.

    :param dirname: The directory name.
    :type dirname: str

    :return: The season ID if found, None otherwise.
    :rtype: Optional[int]
    """
    seasonid_pattern: str = r"Season (\d+)"
    seasonid_match: Optional[re.Match] = re.search(seasonid_pattern, dirname)

    if seasonid_match:
        return int(seasonid_match.group(1))
    return None


def get_video_codec(file_path: str) -> str:
    """
    Get the video codecs from an MP4 file.

    :param file_path: The path to the MP4 file.
    :return: A dictionary with the video and audio codecs.
    """
    try:
        probe = ffmpeg.probe(file_path)

        return next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )["codec_name"]
    except Exception:
        return "unknown"


def get_audio_codec(file_path: str) -> str:
    """
    Get the audio codecs from an MP4 file.

    :param file_path: The path to the MP4 file.
    :return: A dictionary with the video and audio codecs.
    """
    try:
        probe = ffmpeg.probe(file_path)

        return next(
            stream for stream in probe["streams"] if stream["codec_type"] == "audio"
        )["codec_name"]
    except Exception:
        return "unknown"


def get_duration(file_path: str) -> float:
    """
    Get the duration of a movie file in seconds.

    :param file_path: The path to the movie file.
    :return: The duration of the movie file in seconds.
    """
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe["format"]["duration"])
        return duration
    except Exception:
        return 0.0


def get_resolution(file_path: str) -> tuple[int, int]:
    """
    Get the resolution of a movie file in pixels.

    :param file_path: The path to the movie file.
    :return: The resolution of the movie file in pixels.
    """
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        return width, height
    except Exception:
        return 0, 0


def get_bitrate(file_path: str) -> int:
    """
    Get the bitrate of a movie file in kbps.

    :param file_path: The path to the movie file.
    :return: The bitrate of the movie file in kbps.
    """
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )
        bitrate = int(video_stream["bit_rate"]) // 1000
        return bitrate
    except Exception:
        return 0


def get_frame_rate(file_path: str) -> int:
    """
    Get the frame rate of a movie file in frames per second.

    :param file_path: The path to the movie file.
    :return: The frame rate of the movie file in frames per second.
    """
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )
        frame_rate = int(video_stream["r_frame_rate"].split("/")[0])
        return frame_rate
    except Exception:
        return 0


def get_format_name(file_path: str) -> str:
    """
    Get the format name of a movie file.

    :param file_path: The path to the movie file.
    :return: The format name of the movie file.
    """
    try:
        probe = ffmpeg.probe(file_path)
        format_name = probe["format"]["format_name"]
        return format_name
    except Exception:
        return "unknown"


def get_number_of_streams(file_path: str) -> int:
    """
    Get the number of streams in a movie file.

    :param file_path: The path to the movie file.
    :return: The number of streams in the movie file.
    """
    try:
        probe = ffmpeg.probe(file_path)
        number_of_streams = len(probe["streams"])
        return number_of_streams
    except Exception:
        return 0


def get_pixel_format(file_path: str) -> str:
    """
    Get the pixel format of a movie file.

    :param file_path: The path to the movie file.
    :return: The pixel format of the movie file.
    """
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        )
        pixel_format = video_stream["pix_fmt"]
        return pixel_format
    except Exception:
        return "unknown"


def collect_video_file_data(file_path: str) -> VideoFile:
    """
    Collects the video file data.

    :param file_path: The path to the video file.
    :return: VideoFile object.
    """
    [resolution_width, resolution_height] = get_resolution(file_path)

    return VideoFile(
        _filepath=file_path,
        _format_name=get_format_name(file_path),
        _filesize=os.path.getsize(file_path),
        _duration=get_duration(file_path),
        _resolution_width=resolution_width,
        _resolution_height=resolution_height,
        _video_codec=get_video_codec(file_path),
        _audio_codec=get_audio_codec(file_path),
        _bitrate=get_bitrate(file_path),
        _frame_rate=get_frame_rate(file_path),
        _number_of_streams=get_number_of_streams(file_path),
        _pixel_format=get_pixel_format(file_path),
    )

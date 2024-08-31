"""
This module contains the base classes for the configuration and pipeline.
"""

from abc import abstractmethod
from typing import Optional

from loguru import logger
from pandas import DataFrame


def is_not_empty(df: Optional[DataFrame]) -> bool:
    """
    Check if the DataFrame is not empty.

    :param df: The DataFrame to check.
    :return: True if the DataFrame is not empty, False otherwise.
    """
    return not is_empty(df)


def is_empty(df: Optional[DataFrame]) -> bool:
    """
    Check if the DataFrame is empty.

    :param df: The DataFrame to check.
    :return: True if the DataFrame is empty, False otherwise.
    """
    return df is None or df.empty


def pipeline_runner(func):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "config") or self.config is None:
            raise AttributeError(
                "The 'config' property must be set before running the pipeline."
            )
        logger.info(f"Starting {func.__name__} method.")
        result = func(self, *args, **kwargs)
        logger.info(f"Finished {func.__name__} method.")
        return result

    return wrapper


class BaseLibraryConfig:
    """
    This class represents the base configuration for the pipelines.
    """

    _library_name: str
    _library_path: str
    _data_path: str
    _execution_start_time: str
    _execution_end_time: str

    def __init__(self, library_name: str, library_path: str, data_path: str):
        self._library_name = library_name
        self._library_path = library_path
        self._data_path = data_path

    @property
    def library_name(self) -> str:
        """
        Returns the name of the library.

        :return: The name of the library.
        :rtype: str
        """
        return self._library_name

    @property
    def library_path(self) -> str:
        """
        Returns the path to the library.

        :return: The path to the library.
        :rtype: str
        """
        return self._library_path

    @property
    def data_path(self) -> str:
        """
        Returns the path to the data.

        :return: The path to the data.
        :rtype: str
        """
        return self._data_path

    @property
    def execution_start_time(self) -> str:
        """
        Returns the start time of the execution.

        :return: The start time of the execution.
        :rtype: str
        """
        return self._execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, value: str) -> None:
        """
        Sets the start time of the execution.

        :param value: The start time of the execution.
        :type value: str
        :return: None
        """
        self._execution_start_time = value

    @property
    def execution_end_time(self) -> str:
        """
        Returns the end time of the execution.

        :return: The end time of the execution.
        :rtype: str
        """
        return self._execution_end_time

    @execution_end_time.setter
    def execution_end_time(self, value: str) -> None:
        """
        Sets the end time of the execution.

        :param value: The end time of the execution.
        :type value: str
        :return: None
        """
        self._execution_end_time = value


class BasePipeline:
    """
    This class represents the base pipeline for processing libraries.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method to run the pipeline. Must be implemented by subclasses.

        :return: None
        """
        pass

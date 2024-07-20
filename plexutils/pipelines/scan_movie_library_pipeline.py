"""
This module contains the ScanMovieLibraryPipeline class.
"""


class ScanMovieLibraryPipeline:
    """
    This class represents a pipeline for scanning a movie library.
    """

    _library_path: str

    def __init__(self, library_path: str):
        self._library_path = library_path

    def run(self) -> None:
        """
        Runs the pipeline.

        :return: None
        """

        self.collect_data()
        self.load_and_validate_data()
        self.project_and_save_data()

        pass

    def collect_data(self) -> None:
        """
        This method collects the file information from the movie library and saves them to a parquet
        file.

        :return: None
        """
        pass

    def load_and_validate_data(self) -> None:
        """
        This method loads the list of movie files from a parquet file into a list of Movie objects
        and validates them.

        :return: None
        """
        pass

    def project_and_save_data(self) -> None:
        """
        This method projects the list of the Movie objects & invalid files and saves them to a
        parquet file.

        :return: None
        """
        pass

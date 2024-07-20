"""
This module contains the ScanMovieLibraryPipeline class.
"""

import json
import os

from plexutils.media.video_file import VideoFile


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
        movie_directories: list[str] = os.listdir(self._library_path)
        movies: list[VideoFile] = []

        for movie_dir in movie_directories:
            filepath: str = os.path.normpath(
                os.path.join(self._library_path, movie_dir)
            )
            filesize: int = os.path.getsize(filepath)
            movies.append(
                VideoFile(
                    _filepath=filepath,
                    _filesize=filesize,
                    _duration=0,
                    _resolution_width=0,
                    _resolution_height=0,
                    _video_codec="",
                    _audio_codec="",
                )
            )

        print(json.dumps([movie.__dict__ for movie in movies], indent=4))

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


if __name__ == "__main__":

    script_path: str = os.path.dirname(os.path.realpath(__file__))
    pj_path: str = os.path.join(script_path, "..", "..")
    movie_lib = os.path.join(pj_path, "data", "movies", "movies")

    pipeline = ScanMovieLibraryPipeline(os.path.normpath(movie_lib))
    pipeline.run()

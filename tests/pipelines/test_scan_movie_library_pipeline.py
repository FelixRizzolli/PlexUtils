"""
Test the pipeline for scanning the movie library.
"""

import os
import unittest

from plexutils.pipelines.scan_movie_library_pipeline import (
    ScanMovieLibraryPipeline,
    ScanMovieLibraryConfig,
)


class TestScanMovieLibraryPipeline(unittest.TestCase):
    """
    Test the pipeline for the movie library.
    """

    _data_path: str

    def setUp(self):
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")
        self._data_path = os.path.normpath(os.path.join(pj_path, "data", "raw"))

    def test_scan_de_xx_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Anime.

        :return: None
        """
        library_name: str = "[DE-XX] Anime"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_kids_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Kids.

        :return: None
        """
        library_name: str = "[DE-XX] Kids"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_movies_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Movies.

        :return: None
        """
        library_name: str = "[DE-XX] Movies"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_movies_old_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Movies (Old).

        :return: None
        """
        library_name: str = "[DE-XX] Movies (Old)"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_movies_trash_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Movies (Trash).

        :return: None
        """
        library_name: str = "[DE-XX] Movies (Trash)"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_en_xx_movies_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [EN-XX] Movies.

        :return: None
        """
        library_name: str = "[EN-XX] Movies"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_jp_de_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [JP-DE] Anime.

        :return: None
        """
        library_name: str = "[JP-DE] Anime"
        library_path = f"/Volumes/PlexLibrary/Movies/{library_name}"
        self.run_pipeline(library_name, library_path)

    def run_pipeline(self, library_name: str, library_path: str) -> None:
        """
        Run the pipeline for the given library.

        :param library_name: The name of the library.
        :param library_path: The path to the library.
        :return: None
        """
        pipeline_config = ScanMovieLibraryConfig(
            library_name=library_name,
            library_path=library_path,
            data_path=os.path.normpath(self._data_path),
        )
        pipeline = ScanMovieLibraryPipeline(pipeline_config)
        pipeline.run()


if __name__ == "__main__":
    unittest.main()

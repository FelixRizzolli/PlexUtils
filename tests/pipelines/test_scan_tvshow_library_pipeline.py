import os
import unittest

from plexutils.pipelines.scan_tvshow_library_pipeline import (
    ScanTvShowLibraryConfig,
    ScanTvShowLibraryPipeline,
)


class TestScanTvShowLibraryPipeline(unittest.TestCase):

    _data_path: str

    def setUp(self):
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        pj_path: str = os.path.join(script_path, "..", "..")
        self._data_path = os.path.normpath(os.path.join(pj_path, "data", "raw"))

    def test_scan_de_xx_animationsserien_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Animationsserien.

        :return: None
        """
        library_name: str = "[DE-XX] Animationsserien"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Anime.

        :return: None
        """
        library_name: str = "[DE-XX] Anime"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_kids_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Kids.

        :return: None
        """
        library_name: str = "[DE-XX] Kids"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_reality_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Reality & Sitcom.

        :return: None
        """
        library_name: str = "[DE-XX] Reality & Sitcom"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_de_xx_serien_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [DE-XX] Serien.

        :return: None
        """
        library_name: str = "[DE-XX] Serien"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_en_xx_animationsserien_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [EN-XX] Animationsserien.

        :return: None
        """
        library_name: str = "[EN-XX] Animationsserien"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_en_xx_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [EN-XX] Anime.

        :return: None
        """
        library_name: str = "[EN-XX] Anime"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_en_xx_reality_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [EN-XX] Reality & Sitcom.

        :return: None
        """
        library_name: str = "[EN-XX] Reality & Sitcom"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_en_xx_serien_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [EN-XX] Serien.

        :return: None
        """
        library_name: str = "[EN-XX] Serien"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_jp_de_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [JP-DE] Anime.

        :return: None
        """
        library_name: str = "[JP-DE] Anime"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def test_scan_jp_en_anime_library_pipeline(self) -> None:
        """
        Test the pipeline for the library [JP-EN] Anime.

        :return: None
        """
        library_name: str = "[JP-EN] Anime"
        library_path = f"/Volumes/PlexLibrary/TVShows/{library_name}"
        self.run_pipeline(library_name, library_path)

    def run_pipeline(self, library_name: str, library_path: str) -> None:
        """
        Run the pipeline for the given library.

        :param library_name: The name of the library.
        :param library_path: The path to the library.
        :return: None
        """
        pipeline_config = ScanTvShowLibraryConfig(
            library_name=library_name,
            library_path=library_path,
            data_path=os.path.normpath(self._data_path),
        )
        pipeline = ScanTvShowLibraryPipeline(pipeline_config)
        pipeline.run()


if __name__ == "__main__":
    unittest.main()

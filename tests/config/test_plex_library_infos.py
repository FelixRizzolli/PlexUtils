"""
This module contains the TestPlexLibraryInfos class which is used to test the
PlexLibraryInfos class.
"""

import unittest

from plexutils.config.plex_library_infos import PlexLibraryInfos, PlexLibraryType


class TestPlexLibraryInfos(unittest.TestCase):
    """
    Represents a test suite for the PlexLibraryInfos class.
    """

    def test_type_peoperty(self) -> None:
        """
        Test the type property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("movie", plex_info.type)

    def test_name_peoperty(self) -> None:
        """
        Test the name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("Movies", plex_info.name)

    def test_path_peoperty(self) -> None:
        """
        Test the path property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("/path/to/movies", plex_info.path)

    def test_dub_lang_peoperty(self) -> None:
        """
        Test the dub_lang property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("en", plex_info.dub_lang)

    def test_sub_lang_peoperty(self) -> None:
        """
        Test the sub_lang property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("fr", plex_info.sub_lang)

    def test_full_name_peoperty_with_dub2_sub2(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr",
        )
        self.assertEqual("(EN-FR) Movies", plex_info.full_name)

    def test_full_name_peoperty_with_dub5_sub2(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en_US",
            sub_lang="fr",
        )
        self.assertEqual("(US-FR) Movies", plex_info.full_name)

    def test_full_name_peoperty_with_dub2_sub5(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en",
            sub_lang="fr_FR",
        )
        self.assertEqual("(EN-FR) Movies", plex_info.full_name)

    def test_full_name_peoperty_with_dub5_sub5(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            dub_lang="en_US",
            sub_lang="fr_FR",
        )
        self.assertEqual("(US-FR) Movies", plex_info.full_name)

    def test_full_name_peoperty_with_dubnone_sub5(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE,
            name="Movies",
            path="/path/to/movies",
            sub_lang="fr_FR",
        )
        self.assertEqual("(EN-FR) Movies", plex_info.full_name)

    def test_full_name_peoperty_with_dubnone_subnone(self) -> None:
        """
        Test the full_name property.
        """
        plex_info = PlexLibraryInfos(
            type=PlexLibraryType.MOVIE, name="Movies", path="/path/to/movies"
        )
        self.assertEqual("(EN) Movies", plex_info.full_name)


if __name__ == "__main__":
    unittest.main()

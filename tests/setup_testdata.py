"""
    This module contains methods in form of unit tests for setting up a test environment.
"""
import os
import unittest

from tests.testdata import test_movie_files, test_tvshow_files

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../data')
movies_dir = os.path.join(data_dir, 'movies')
tvshows_dir = os.path.join(data_dir, 'tvshows')


def delete_directory(dir_path):
    """deletes the given directory and all its contents"""
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)
    os.rmdir(dir_path)


class SetupTestData(unittest.TestCase):
    """this class contains methods in form of unit tests for setting up a test environment"""

    def test_create_movie_files(self):
        """creates the movies files for the tests"""
        movie_files = test_movie_files

        # clear data
        if os.path.isdir(movies_dir):
            delete_directory(movies_dir)

        # create data
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(movies_dir):
            os.mkdir(movies_dir)

        for movie_file in movie_files:
            open(os.path.join(movies_dir, movie_file), 'a').close()

        self.assertTrue(os.path.isdir(movies_dir))

    def test_create_tvshow_files(self):
        """creates the tv show directories and files for the tests"""
        tvshow_directories = test_tvshow_files

        # clear data
        if os.path.isdir(tvshows_dir):
            delete_directory(tvshows_dir)

        # create data
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(tvshows_dir):
            os.mkdir(tvshows_dir)

        for tvshow in tvshow_directories:
            tvshow_dirname = tvshow["dirname"]
            tvshow_dir = os.path.join(tvshows_dir, tvshow_dirname)
            if not os.path.isdir(tvshow_dir):
                os.mkdir(tvshow_dir)

            for season in tvshow["seasons"]:
                season_dirname = season["dirname"]
                season_dir = os.path.join(tvshow_dir, season_dirname)
                if not os.path.isdir(season_dir):
                    os.mkdir(season_dir)

                for episode in season["episodes"]:
                    episode_dir = os.path.join(season_dir, episode)
                    open(episode_dir, 'a').close()

        self.assertTrue(os.path.isdir(tvshows_dir))

import unittest
import os

from plex_movie_crawler import PlexMovieCrawler
from test_data import test_movie_files

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
movies_dir = os.path.join(data_dir, 'movies')


def delete_directory(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)
    os.rmdir(dir_path)


class TestPlexMovieCrawler(unittest.TestCase):

    def setUp(self):
        self.movie_files = test_movie_files

        # clear data
        if os.path.isdir(movies_dir):
            delete_directory(movies_dir)

        # create data
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(movies_dir):
            os.mkdir(movies_dir)

        for movie_file in self.movie_files:
            open(os.path.join(movies_dir, movie_file), 'a').close()

        # initialize crawler
        self.crawler = PlexMovieCrawler(movies_dir)
        self.crawler.crawl()

    def test_crawl_get_movies_count(self):
        movies = self.crawler.get_movies()
        invalid_movies = self.crawler.get_invalid_movies()
        self.assertEqual(len(self.movie_files), len(movies) + len(invalid_movies))

    def test_crawl_get_movies_object(self):
        movies = self.crawler.get_movies()
        matrix1 = list(filter(lambda movie: movie["filename"] == "The Matrix (1999) {tvdb-169}.mp4", movies))[0]
        self.assertEqual(matrix1["filename"], "The Matrix (1999) {tvdb-169}.mp4")
        self.assertEqual(matrix1["id"], "169")

    def test_crawl_get_invalid_movie(self):
        invalid_movies = self.crawler.get_invalid_movies()
        self.assertEqual("Baby Driver (2017).mp4", invalid_movies[0])


if __name__ == '__main__':
    unittest.main()

import unittest
import os

from plex_movie_crawler import PlexMovieCrawler

current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
movies_dir = os.path.join(data_dir, 'movies')

class TestPlexMovieCrawler(unittest.TestCase):

    def setUp(self):
        self.movie_files = [
            "The Matrix (1999) {tvdb-169}.mp4",
            "The Matrix Reloaded (2003) {tvdb-553}.mp4",
            "The Matrix Revolutions (2003) {tvdb-687}.mp4",
            "The Matrix Resurrections (2021) {tvdb-131590}.mp4",
            "Happy Death Day (2017) {tvdb-475}.mp4",
            "Baby Driver (2017).mp4",
        ]

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        if not os.path.isdir(movies_dir):
            os.mkdir(movies_dir)

        for movie_file in self.movie_files:
            open(os.path.join(movies_dir, movie_file), 'a').close()

        self.crawler = PlexMovieCrawler(movies_dir)
        self.crawler.crawl()

    def test_crawl_get_movies_count(self):
        movies = self.crawler.get_movies()
        self.assertEqual(len(self.movie_files), len(movies))

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

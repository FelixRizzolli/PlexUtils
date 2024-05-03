import json
import os

from movie import Movie
from movie_list import MovieList

class PlexMovieCrawler(object):
    def __init__(self, path):
        self.invalid_movies = None
        self.movies = None
        self.path = path

    def crawl(self):
        movie_directories = os.listdir(self.path)

        self.movies = MovieList()
        self.invalid_movies = []

        for movie_dir in movie_directories:
            movie = Movie(movie_dir)

            if movie.get_tvdbid() is not None:
                self.movies.add(movie)
            else:
                self.invalid_movies.append(f"{movie_dir}")


    def get_movielist(self):
        return self.movies

    def get_invalid_movies(self):
        return self.invalid_movies
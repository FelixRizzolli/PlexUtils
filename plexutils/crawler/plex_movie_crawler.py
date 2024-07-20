"""
    This module contains PlexMovieCrawler class.
"""

import os

from plexutils.media.movie import Movie
from plexutils.media.movie_list import MovieList


class PlexMovieCrawler:
    """class for crawling movie data from a plex library"""

    def __init__(self, path):
        self.invalid_movies: list[str] = []
        self.movielist: MovieList = MovieList()
        self.path = path

    def crawl(self) -> None:
        """
        crawls the movies from a plex library

        :return: None
        """
        movie_directories: list[str] = os.listdir(self.path)

        for movie_dir in movie_directories:
            movie: Movie = Movie(movie_dir)

            if movie.tvdbid is not None:
                self.movielist.add(movie)
            else:
                self.invalid_movies.append(f"{movie_dir}")

    def get_movielist(self) -> MovieList:
        """
        returns the list of all movies

        :return: The list of all movies
        :rtype: MovieList
        """
        return self.movielist

    def get_invalid_movies(self) -> list[str]:
        """
        returns the list of invalid movies

        :return: The list of invalid movies
        :rtype: list[str]
        """
        return self.invalid_movies

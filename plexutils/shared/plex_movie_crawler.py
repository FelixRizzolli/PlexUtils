"""
    This module contains PlexMovieCrawler class.
"""
import os
from typing import List

from plexutils.media.movie import Movie
from plexutils.media.movie_list import MovieList


class PlexMovieCrawler:
    """class for crawling movie data from a plex library"""

    def __init__(self, path):
        self.invalid_movies: List[str] = []
        self.movielist: MovieList = MovieList()
        self.path = path

    def crawl(self) -> None:
        """crawls the movies from a plex library"""
        movie_directories: List[str] = os.listdir(self.path)

        for movie_dir in movie_directories:
            movie: Movie = Movie(movie_dir)

            if movie.get_tvdbid() is not None:
                self.movielist.add(movie)
            else:
                self.invalid_movies.append(f"{movie_dir}")

    def get_movielist(self) -> MovieList:
        """returns the list of all movies"""
        return self.movielist

    def get_invalid_movies(self) -> List[str]:
        """returns the list of invalid movies"""
        return self.invalid_movies

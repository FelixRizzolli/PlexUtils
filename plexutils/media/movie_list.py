"""
This module contains MovieList class.
"""

from dataclasses import dataclass
from typing import Optional

from plexutils.media.movie import Movie


@dataclass
class MovieList:
    """
    Represents a collection of movies.
    """

    def __init__(self):
        self._movies: dict[int, Movie] = {}

    @property
    def movies(self) -> list[Movie]:
        """
        Returns all movies in the collection.

        :return: A list of all movies in the collection.
        :rtype: list[Movie]
        """
        return list(self._movies.values())

    def add(self, movie: Movie) -> None:
        """
        Adds a movie to the collection.

        :param movie: The movie to add.
        :type movie: Movie
        """
        if movie.tvdbid is None:
            raise ValueError("Movie TVDB ID is required")
        if movie.tvdbid in self._movies:
            raise ValueError(f"Movie with TVDB ID {movie.tvdbid} already exists")

        self._movies[movie.tvdbid] = movie

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        """
        Returns the movie with the given ID.

        :param movie_id: The TVDB ID of the movie to return.
        :type movie_id: int

        :return: The movie with the given ID, or None if no such movie exists.
        :rtype: Optional[Movie]
        """
        return self._movies.get(movie_id)

    def is_empty(self) -> bool:
        """
        Checks if the collection is empty.

        :return: True if the collection is empty, False otherwise.
        :rtype: bool
        """
        return len(self._movies) == 0

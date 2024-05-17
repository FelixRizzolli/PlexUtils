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

    Attributes:
        _movies (dict[int, Movie]): A dictionary mapping TVDB IDs to movies.
    """

    def __init__(self):
        self._movies: dict[int, Movie] = {}

    @property
    def movies(self) -> list[Movie]:
        """
        Returns all movies in the collection.

        Returns:
            list[Movie]: A list of all movies in the collection.
        """
        return list(self._movies.values())

    def add(self, movie: Movie) -> None:
        """
        Adds a movie to the collection.

        Args:
            movie (Movie): The movie to add.
        """
        self._movies[movie.tvdbid] = movie

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        """
        Returns the movie with the given ID.

        Args:
            movie_id (int): The TVDB ID of the movie to return.

        Returns:
            Optional[Movie]: The movie with the given ID, or None if no such movie exists.
        """
        return self._movies.get(movie_id)

    def is_empty(self) -> bool:
        """
        Checks if the collection is empty.

        Returns:
            bool: True if the collection is empty, False otherwise.
        """
        return len(self._movies) == 0

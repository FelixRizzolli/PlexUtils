"""
    This module contains MovieList class.
"""


class MovieList:
    """represents a collection of movies"""

    def __init__(self):
        self.movies = []

    def add(self, movie):
        """adds a movie to the collection"""
        self.movies.append(movie)

    def get_movies(self):
        """returns all movies in the collection"""
        return self.movies

    def get_movie(self, movie_id):
        """returns the movie with the given id"""
        for movie in self.movies:
            if movie.get_tvdbid() == movie_id:
                return movie
        return None

    def is_empty(self):
        """checks if collection is empty"""
        return len(self.movies) == 0

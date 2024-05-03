
class MovieList:
    def __init__(self):
        self.movies = []

    def add(self, movie):
        self.movies.append(movie)

    def get_movies(self):
        return self.movies

    def get_movie(self, movie_id):
        for movie in self.movies:
            if movie.get_tvdbid() == movie_id:
                return movie
        return None

    def is_empty(self):
        return len(self.movies) == 0
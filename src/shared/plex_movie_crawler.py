import json
import os
import re

tvdb_id_pattern = r'{tvdb-(\d+)}'

class PlexMovieCrawler(object):
    def __init__(self, path):
        self.invalid_movies = None
        self.movies = None
        self.path = path

    def crawl(self):
        files = os.listdir(self.path)

        self.movies = []
        self.invalid_movies = []

        for file in files:
            match = re.search(tvdb_id_pattern, file)
            if match:
                movie = {
                    "id": match.group(1),
                    "filename": file,
                }
                self.movies.append(movie)
            else:
                self.invalid_movies.append(file)


    def get_movies(self):
        return self.movies

    def get_invalid_movies(self):
        return self.invalid_movies
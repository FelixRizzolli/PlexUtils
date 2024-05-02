import os

class PlexMovieCrawler(object):
    def __init__(self, path):
        self.movies = None
        self.path = path

    def crawl(self):
        files = os.listdir(self.path)
        self.movies = files

    def get_movies(self):
        return self.movies

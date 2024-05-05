from plexutils.shared.utils import extract_tvdbid


class Movie:
    """represents a single movie"""
    def __init__(self, filename):
        self.filename = filename
        self.tvdbid = extract_tvdbid(filename)

    def get_tvdbid(self):
        """returns the tvdbid of the movie"""
        return self.tvdbid

    def get_filename(self):
        """return the filename of the movie"""
        return self.filename

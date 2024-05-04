from plexutils.shared.utils import extract_tvdbid


class Movie:
    def __init__(self, filename):
        self.filename = filename
        self.tvdbid = extract_tvdbid(filename)

    def get_tvdbid(self):
        return self.tvdbid

    def get_filename(self):
        return self.filename

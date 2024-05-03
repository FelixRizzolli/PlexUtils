
class TVShowList:
    def __init__(self):
        self.tvshows = []

    def add_tvshow(self, tvshow):
        self.tvshows.append(tvshow)

    def get_tvshows(self):
        return self.tvshows

    def get_tvshow(self, tvshow_id):
        for tvshow in self.tvshows:
            if tvshow.get_tvdbid() == tvshow_id:
                return tvshow

    def is_empty(self):
        return len(self.tvshows) == 0


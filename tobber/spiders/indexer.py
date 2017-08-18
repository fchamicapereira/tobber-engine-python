import scrapy

class Indexer(scrapy.Spider):
    def __init__(self, title=None, season=None, *args, **kwargs):
        super(Indexer, self).__init__(*args, **kwargs)

        # title will not be a string, but a list
        # this allows me to make more than 1 request
        # when I want to, like searching for "season 1" and "s01"

        self.title = []

        if season != -1:

            # search for, for example, "game of thrones season 1" or "game of thrones s01"
            if season < 10:
                keywords = [' season ',' s0']
            else:
                keywords = [' season ',' s']

            for k in keywords:
                self.title.append((title + k + str(season)).replace(' ','%20'))

        else:
            self.title.append(title)

import scrapy

class Indexer(scrapy.Spider):
    def __init__(self, title=None, *args, **kwargs):
        super(Indexer, self).__init__(*args, **kwargs)
        self.title = title

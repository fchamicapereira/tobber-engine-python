import scrapy
from scrapy.exceptions import DropItem

# Dump raw anime
class English_anime(object):
    def process_item(self, item, spider):
        avoid = [
            'non',
            'raw',
            'audio'
        ]

        # only anime torrents have a category

        if 'category' in item and item['category'] != None:
            if all(words not in item['category'].lower() for words in avoid):
                return item

        raise DropItem('Only english translated anime is desirable')

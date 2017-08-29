import scrapy
from scrapy.exceptions import DropItem

# Dump raw anime
class Check_search(object):
    def process_item(self, item, spider):
        for search in spider.title:
            words = search.split('%20')
            for w in words:
                if w.lower() not in item['title'].lower():
                    raise DropItem('Title does not match the content searched')
        return item

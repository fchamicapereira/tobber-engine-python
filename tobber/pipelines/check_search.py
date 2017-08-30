import scrapy
import re
from scrapy.exceptions import DropItem

# Dump raw anime
class Check_search(object):
    def process_item(self, item, spider):

        found = False
        separators = ['%20', '_', '.', '-', '+', '(', ')']
        title = item['title'].lower()
        spider_title = [w.replace('%20', ' ').split(' ') for w in spider.title]

        for s in separators:
            title = title.replace(s,' ')

        for search in spider_title:

            if 'season' in search:
                season = search[search.index('season') + 1]
                search.append(' season ' + season + ' ')

                if season < 10:
                    search.append(' season 0' + season + ' ')

        for search in spider_title:

            if all(word in title for word in search):
                return item

        raise DropItem('Title does not match the content searched')

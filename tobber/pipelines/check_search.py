import scrapy
import re
from scrapy.exceptions import DropItem

# Dump raw anime
class Check_search(object):
    def process_item(self, item, spider):

        found = False
        separators = ['%20', '_', '.', '-', '+']
        title = item['title'].lower()
        spider_title = [w.replace('%20', ' ') for w in spider.title]

        for s in separators:
            title = title.replace(s,' ')

        for search in spider_title:

            if len(re.findall(r'season \d+', search)) > 0:
                spider_title.append('season ' + re.findall(r'\d+',re.findall(r'season \d+',search)[0])[0])
                break

            if len(re.findall(r's\d+', search)) > 0:
                spider_title.append('s' + re.findall(r'\d+',re.findall(r's \d+',search)[0])[0])
                break

        for search in spider.title:

            words_in_search = search.split('%20')

#            print title,words_in_search

            if all(word in title for word in words_in_search):
                return item

        raise DropItem('Title does not match the content searched')

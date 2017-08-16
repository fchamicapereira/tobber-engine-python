import scrapy
import json

class Sort(object):

    def __init__(self):
        self.items = []

    def close_spider(self, spider):
        ordered = sorted(self.items, key=lambda item: item['score'], reverse=True)

        for i in range(5):
            print '----------------------------------'
            print 'Place: ', i + 1
            print json.dumps(ordered[i], indent=4, sort_keys=True)

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

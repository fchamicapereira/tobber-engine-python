import scrapy
import json

class Print(object):

    def process_item(self, item, spider):
        print json.dumps(dict(item),indent=4,sort_keys=True)
        return item

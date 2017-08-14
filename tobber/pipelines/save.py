import scrapy
import json


# Save all data in file
class Save(object):
    def open_spider(self, spider):
        self.file = open('torrents.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
